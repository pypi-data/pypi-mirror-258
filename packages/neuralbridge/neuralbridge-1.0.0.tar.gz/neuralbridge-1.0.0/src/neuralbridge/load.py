"""
Neural Bridge
=============

Function: constants
"""

from onnx.onnx_ml_pb2 import ModelProto as Model_onnx
from tensorflow import Module as Model_tf
from torch.nn import Module as Model_torch

from .constants import ONNX_MODEL, TF_MODEL, TORCH_MODEL
from .constants import SupportedModel
from .functions_ import get_model_type_, onnx_to_tf_, onnx_to_torch_
from .functions_ import tf_to_onnx_, torch_to_onnx_


def load_as(model: SupportedModel, output_type: str) -> SupportedModel:
    """Load model as the specified type

    Parameters
    ----------
    model : SupportedModel
        Model to load
    output_type : str
        Type of the model to load as

    Returns
    -------
    SupportedModel
        The loaded model with type according to the output_type parameter

    Raises
    ------
    RuntimeError
        When unsupported model type is given.
    """

    if output_type == ONNX_MODEL:
        return load_as_onnx(model)
    elif output_type == TF_MODEL:
        return load_as_tf(model)
    elif output_type == TORCH_MODEL:
        return load_as_torch(model)
    else:
        raise RuntimeError(f'Unsupported output type "{output_type}".')


def load_as_onnx(model: SupportedModel) -> Model_onnx:
    """Load model as ONNX Model

    Parameters
    ----------
    model : SupportedModel
        Model to load

    Returns
    -------
    Model_onnx
        The loaded ONNX model
    """

    model_type_ = get_model_type_(model)
    if model_type_ == TF_MODEL:
        return tf_to_onnx_(model, None)
    elif model_type_ == TORCH_MODEL:
        return torch_to_onnx_(model, None, None, None)
    elif model_type_ == ONNX_MODEL:
        return model


def load_as_tf(model: SupportedModel) -> Model_tf:
    """Load model as TensorFlow Model

    Parameters
    ----------
    model : SupportedModel
        Model to load

    Returns
    -------
    Model_tf
        The loaded TensorFlow model
    """

    model_type_ = get_model_type_(model)
    if model_type_ == TORCH_MODEL:
        onnx_model_ = torch_to_onnx_(model, None, None, None)
        return onnx_to_tf_(onnx_model_)
    elif model_type_ == ONNX_MODEL:
        return onnx_to_tf_(model)
    elif model_type_ == TF_MODEL:
        return model


def load_as_torch(model: SupportedModel) -> Model_torch:
    """PyTorch

    Parameters
    ----------
    model : SupportedModel
        Model to load

    Returns
    -------
    Model_torch
        The loaded PyTorch model
    """

    model_type_ = get_model_type_(model) 
    if model_type_ == TF_MODEL:
        onnx_model_ = tf_to_onnx_(model, None)
        return onnx_to_torch_(onnx_model_)
    elif model_type_ == ONNX_MODEL:
        return tf_to_onnx_(model, None)
    elif model_type_ == TORCH_MODEL:
        return model