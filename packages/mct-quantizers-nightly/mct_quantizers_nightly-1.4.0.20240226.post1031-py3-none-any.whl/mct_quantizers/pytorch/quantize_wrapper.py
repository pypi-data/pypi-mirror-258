# Copyright 2023 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================f
from typing import List, Union, Any, Dict, Tuple

import inspect

from mct_quantizers.common.base_inferable_quantizer import BaseInferableQuantizer
from mct_quantizers.common.constants import FOUND_TORCH, LAYER, TRAINING
from mct_quantizers.logger import Logger

if FOUND_TORCH:
    import torch
    import torch.nn as nn


    class PytorchQuantizationWrapper(nn.Module):
        def __init__(self,
                     module: nn.Module,
                     weights_quantizers: Dict[str, BaseInferableQuantizer] = None):
            """
            Pytorch Quantization Wrapper takes a pytorch module and quantizers and infer a quantized module.

            Args:
                module: A pytorch module.
                weights_quantizers: A dictionary between a weight's name to its quantizer.
            """
            super().__init__()
            if isinstance(module, nn.Module):
                self.add_module(LAYER, module)
            else:
                # Functional layers
                setattr(self, LAYER, module)

            self.weights_quantizers = weights_quantizers if weights_quantizers is not None else dict()
            self._set_weights_vars(True)

        def add_weights_quantizer(self, param_name: str, quantizer: BaseInferableQuantizer):
            """
            This function adds a weights quantizer to existing wrapper

            Args:
                param_name: The name of the parameter to quantize
                quantizer: A quantizer.

            Returns: None

            """
            self.weights_quantizers.update({param_name: quantizer})

        @property
        def is_weights_quantization(self) -> bool:
            """
            This function check weights quantizer exists in wrapper.

            Returns: a boolean if weights quantizer exists

            """
            return self.num_weights_quantizers > 0

        @property
        def num_weights_quantizers(self) -> int:
            """
            Returns: number of weights quantizers
            """
            return len(self.weights_quantizers)

        def convert_to_inferable_quantizers(self):
            """
            Convert the wrapper quantizers with inferable quantizers

            """
            # Weight quantizers
            if self.is_weights_quantization:
                inferable_weight_quantizers = {}
                for name, quantizer in self.weights_quantizers.items():
                    if hasattr(quantizer, 'convert2inferable') and callable(quantizer.convert2inferable):
                        inferable_weight_quantizers.update({name: quantizer.convert2inferable()})
                self.weights_quantizers = inferable_weight_quantizers
                self._set_weights_vars(False)

        def _set_weights_vars(self, is_training: bool = True):
            """
            Initialize learnable weights as parameters in the wrapper, and their quantizers

            Args:
                is_training: Whether working with InferableQuantizers or not. If so, do not register weight as parameter.

            """
            self._weights_vars = []

            # Init weights quantizers
            for name, quantizer in self.weights_quantizers.items():
                if is_training:
                    weight = getattr(self.layer, name).detach()
                    delattr(self.layer, name)
                    setattr(self.layer, name, weight)
                    self.register_parameter(name, torch.nn.Parameter(weight, requires_grad=True))
                else:
                    weight = getattr(self, name).detach()
                    delattr(self.layer, name)
                    setattr(self.layer, name, weight)
                quantizer.initialize_quantization(weight.shape, name, self)
                self._weights_vars.append((name, getattr(self, name), quantizer))

        def set_quantize_weights(self, quantized_weights: dict):
            """
            This function updates layer weights after quantization.

            Args:
                quantized_weights: a dict of weight to update

            Returns: None

            """
            for weight_attr in self.weights_quantizers.keys():
                weight = quantized_weights.get(weight_attr)
                setattr(self.layer, weight_attr, weight)

        def get_weights_vars(self) -> List[Tuple[str, Any, BaseInferableQuantizer]]:
            """
            A getter of the layer's weights variables.

            Returns:
                List pf tuples of the wrapped layer's weights variables with weight name, values and assigned quantizer.

            """

            return self._weights_vars

        def forward(self,
                    *args: List[Any],
                    **kwargs: Dict[str, Any]) -> Union[torch.Tensor, List[torch.Tensor]]:
            """
            PytorchQuantizationWrapper forward functions
            Args:
                args: arguments to pass to internal layer.
                kwargs: key-word dictionary to pass to the internal layer.

            Returns: a tensor that simulates a quantized layer.

            """

            # ----------------------------------
            # Quantize all weights, and replace them in the underlying layer.
            # ----------------------------------
            if self.is_weights_quantization:

                quantized_weights = {}
                for name, unquantized_weight, quantizer in self._weights_vars:
                    s = inspect.signature(quantizer.__call__)
                    if TRAINING in s.parameters.keys():
                        quantized_weight = quantizer(unquantized_weight, self.training)
                    else:
                        quantized_weight = quantizer(unquantized_weight)

                    quantized_weights.update({name: quantized_weight})

                self.set_quantize_weights(quantized_weights)


            # ----------------------------------
            # Layer operation
            # ----------------------------------
            outputs = self.layer(*args, **kwargs)

            return outputs

        def get_quantized_weights(self) -> Dict[str, torch.Tensor]:
            """

            Returns: A dictionary of weights attributes to quantized weights.

            """
            quantized_weights = {}
            weights_var = self.get_weights_vars()
            for name, w, quantizer in weights_var:
                quantized_weights[name] = quantizer(w)
            return quantized_weights

else:
    class PytorchQuantizationWrapper(object):
        def __init__(self,
                     layer,
                     weight_quantizers: Dict[str, BaseInferableQuantizer] = None):
            """
            Pytorch Quantization Wrapper takes a pytorch module and quantizers and infer a quantized layer.

            Args:
                layer: A pytorch module.
                weight_quantizers: A dictionary between a weight's name to its quantizer.
            """
            Logger.critical('Installing Pytorch is mandatory '
                            'when using PytorchQuantizationWrapper. '
                            'Could not find torch package.')  # pragma: no cover
