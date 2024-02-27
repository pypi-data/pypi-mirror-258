"""
Neural Bridge
=============

Function: convert_model
"""

from collections.abc import Iterable

from torch import dtype as torch_dtype

from .constants import AUTO_MODEL_TYPE, TF_MODEL, TORCH_MODEL
from .constants import SupportedModel
from .functions_ import get_model_type_, onnx_to_tf_, onnx_to_torch_
from .functions_ import tf_to_onnx_, torch_to_onnx_


def convert_model(model: SupportedModel, *,
                  input_model_type: str = AUTO_MODEL_TYPE,
                  input_model_weights: str | None = None,
                  output_model_type: str = AUTO_MODEL_TYPE,
                  output_name: str | None = None, output_path: str | None = None,
                  save_onnx_output: bool = False,
                  torch_shape: Iterable | None = None,
                  torch_type: torch_dtype | str | None = None) -> SupportedModel:
    """Convert model from a supported model type to another supported model type

    Parameters
    ----------
    model : SupportedModel
        Model to convert
    input_model_type : str, optional
        Expected type to the given model, by default AUTO_MODEL_TYPE
    input_model_weights : str | None, optional
        Path to model weights, if None no weights are loaded, by default None
    output_model_type : str, optional
        Expected output model type, by default AUTO_MODEL_TYPE
    output_name : str | None, optional
        Name of the output model file(s) if set to None, class name will be
        used, by default None
    output_path : str | None, optional
        Path of model files to save to, if set to None, current directory will
        be used, by default None
    save_onnx_output : bool, optional
        Whether to save ONNX model or not, by default False
    torch_shape : Iterable | None, optional
        Input shape for PyTorch model, must be set only if given model is a
        PyTorch model which is not yet converted to ScriptFunction or
        ScriptModel, by default None
    torch_type : torch_dtype | str | None, optional
        Input data type for PyTorch model, must be set only if given model is a
        PyTorch model which is not yet converted to ScriptFunction or
        ScriptModel, by default None

    Returns
    -------
    SupportedModel
        The converted model

    Raises
    ------
    RuntimeError
        When expected given model type and given model type is different. This
        is a way to check real given model type. To avoid this error, leave
        input_model_type parameter to AUTO_MODEL_TYPE (default).
    ValueError
        When output model type is not supported.
    RuntimeError
        When conversion of the given model is not supported because if its type.
    RuntimeError
        When conversion of the output model is not supported because if its type.
    RuntimeError
        When conversion to ONNX model is not supported for the given model based
        on its type.

    Notes
    -----
    To see all the possible errors, read the documentation of the following
    functions:
        .functions_.get_model_type_()
        __determine_output_model_type()
        __load_model_weights()
        .functions_.torch_to_onnx_()
    """

    expected_type_ = __get_expected_input_type(input_model_type)
    input_model_type_ = get_model_type_(model)
    if expected_type_ != AUTO_MODEL_TYPE\
       and input_model_type_ != input_model_type:
        raise RuntimeError(f'Inconsistent types: expected input "{expected_type_}", given input "{input_model_type_}".')
    if output_model_type not in [AUTO_MODEL_TYPE, TF_MODEL, TORCH_MODEL]:
        raise ValueError(f'Unsupported output model type "{output_model_type}".')
    output_model_type_ = __determine_output_model_type(input_model_type_,
                                                       output_model_type)
    output_path_base_ = __get_output_path_base(model, output_name, output_path)
    onnx_path_base_ = output_path_base_ if save_onnx_output else None
    if input_model_weights is not None:
        __load_model_weights(model, input_model_type_, input_model_weights)
    if input_model_type_ != output_model_type_:
        if input_model_type_ == TF_MODEL:
            onnx_model_ = tf_to_onnx_(model, onnx_path_base_)
        elif input_model_type_ == TORCH_MODEL:
            onnx_model_ = torch_to_onnx_(model, torch_shape, torch_type,
                                         onnx_path_base_)
        else:
            raise RuntimeError(f'Conversion for model type "{input_model_type_}" is not supported.')
        if output_model_type_ == TF_MODEL:
            result_ = onnx_to_tf_(onnx_model_)
        elif output_model_type_ == TORCH_MODEL:
            result_ = onnx_to_torch_(onnx_model_)
        else:
            raise RuntimeError(f'Conversion for model type "{input_model_type_}" is not supported.')
    else:
        if save_onnx_output == True:
            if input_model_type_ == TF_MODEL:
                tf_to_onnx_(model, onnx_path_base_)
            elif input_model_type_ == TORCH_MODEL:
                torch_to_onnx_(model, torch_shape, torch_type, onnx_path_base_)
            else:
                raise RuntimeError(f'ONNX export for model type "{input_model_type_}" is not supported.')
        result_ = model
    return result_


def __determine_output_model_type(given_model_type: str,
                                  output_model_type: str) -> str:
    """Determine expected output model type based on given model type and output
    model type parameter

    Parameters
    ----------
    given_model_type : str
        Type of the given model
    output_model_type : str
        The given output type parameter

    Returns
    -------
    str
        Model type that the convert_model() function expects to output

    Raises
    ------
    ValueError
        When the expected output model type cannot get determined. If output
        model type is set to AUTO_MODEL_TYPE, expected output is determined by
        the type of the given model.
    """

    result_ = output_model_type
    if result_ == AUTO_MODEL_TYPE:
        if given_model_type not in [TF_MODEL, TORCH_MODEL]:
            raise ValueError(f'Cannot determine desired output model type because given model is "{given_model_type}".')
        else:
            result_ = TF_MODEL if given_model_type == TORCH_MODEL\
                               else TORCH_MODEL
    return result_


def __get_expected_input_type(input_model_type: str) -> str:
    """Determine the expected model type

    Parameters
    ----------
    input_model_type : str
        Input type parameter set by the user

    Returns
    -------
    str
        Converted model type as input expectation
    """

    return input_model_type if input_model_type in [AUTO_MODEL_TYPE, TF_MODEL,
                                                    TORCH_MODEL]\
                            else AUTO_MODEL_TYPE


def __get_output_path_base(model: SupportedModel, output_name: str | None,
                           output_path: str | None) -> str:
    """_summary_

    Parameters
    ----------
    model : SupportedModel
        The given model
    output_name : str | None
        Output model name, if set to None, class name will be used
    output_path : str | None
        Output path, if set to None, current path will be used

    Returns
    -------
    str
        Path base to use for saving the model
    """

    output_name_ = output_name if output_name is not None\
                               else model.__class__.__name__
    output_path_ = output_path if output_path is not None else './'
    return f'{output_path_.rstrip("/")}/{output_name_}'


def __load_model_weights(model: SupportedModel, model_type: str,
                         path_to_weights: str):
    """Load model weights

    Parameters
    ----------
    model : SupportedModel
        Model to load weights for
    model_type : str
        Type of the model to load weights for
    path_to_weights : str
        Path of the file of the model weights

    Raises
    ------
    RuntimeError
        When loading weights is not supported for the given model.
    """

    if model_type == TF_MODEL:
        model.load_weights(path_to_weights)
    elif model_type == TORCH_MODEL:
        model.load_state_dict(path_to_weights)
    else:
        raise RuntimeError(f'Loading separated weights for model type "{model_type}" is not supported.')