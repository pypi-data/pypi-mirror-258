"""
Neural Bridge
=============

Function: constants

"""

from typing import Union

from onnx.onnx_ml_pb2 import ModelProto as Model_onnx
from tensorflow import Module as Model_tf, Tensor as Tensor_tf
from torch import Tensor as Tensor_torch
from torch.nn import Module as Model_torch


AUTO_MODEL_TYPE = 'auto'
ONNX_MODEL = 'onnx'
TF_MODEL = 'tf'
TORCH_MODEL = 'torch'

SupportedModel = Union[Model_tf, Model_torch, Model_onnx]
SupportedTensor = Union[Tensor_tf, Tensor_torch]