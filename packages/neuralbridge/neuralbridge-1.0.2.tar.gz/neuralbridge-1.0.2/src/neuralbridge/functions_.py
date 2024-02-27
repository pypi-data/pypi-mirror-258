"""
Neural Bridge
=============

Submodule: functions_

"""

from collections.abc import Iterable
from os import remove as os_remove
from shutil import rmtree

from onnx import load as onnx_load, save as onnx_save
from onnx.onnx_ml_pb2 import ModelProto as Model_onnx
from onnx_tf.backend import prepare as convert_onnx_to_tf # pip install tensorflow-probability
from onnx2torch import convert as convert_onnx_to_torch
from tensorflow import Module as Model_tf, saved_model as tf_saved_model
from tf2onnx.convert import from_keras as convert_tf_to_onnx
from torch import dtype as torch_dtype, float32 as torch_float32
from torch import randn as torch_randn
from torch.jit import ScriptFunction as torch_ScriptFunction
from torch.jit import ScriptModule as torch_ScriptModule
from torch.nn import Module as Model_torch
from torch.onnx import export as torch_onnx_export

from .constants import TF_MODEL, TORCH_MODEL
from .constants import SupportedModel


def get_model_type_(model: SupportedModel) -> str:
    """Identify the type of the given model

    Parameters
    ----------
    model : SupportedModel
        Model to identify type of

    Returns
    -------
    str
        The identified model type

    Raises
    ------
    RuntimeError
        When type of the model cannot get identified.
    """

    result_ = TF_MODEL if isinstance(model, Model_tf) else\
              TORCH_MODEL if isinstance(model, Model_torch) else None
    if result_ is None:
        raise RuntimeError('Cannot determine model type. It is unsupported.')
    return result_


def onnx_to_tf_(model: Model_onnx, delete_tmp_dir : bool = True) -> Model_tf:
    """Convert ONNX model to TensorFlow

    Parameters
    ----------
    model : Model_onnx
        ONNX model instance to convert
    delete_tmp_dir : bool, optional
        Whether to delete temporarily created graph directory or not,
        by default True

    Returns
    -------
    Model_tf
        The converted TensorFlow model instance

    Notes
    -----
    This solution is based on:
        https://github.com/onnx/onnx-tensorflow/?tab=readme-ov-file#convert-programmatically
    """

    TMP_DIRECTORY_NAME_ = 'model_tmp_dir'
    convert_onnx_to_tf(model).export_graph(TMP_DIRECTORY_NAME_)
    result_ = tf_saved_model.load(TMP_DIRECTORY_NAME_)
    if delete_tmp_dir:
        __remove_directory(TMP_DIRECTORY_NAME_)
    return result_


def onnx_to_torch_(model: Model_onnx) -> Model_torch:
    """Convert ONNX model to Pytorch

    Parameters
    ----------
    model : Model_onnx
        ONNX model instance to convert

    Returns
    -------
    Model_torch
        The converted PyTorch model instance

    Notes
    -----
    This solution is based on:
        https://github.com/ENOT-AutoDL/onnx2torch
    """

    return convert_onnx_to_torch(model)


def tf_to_onnx_(model: Model_tf, onnx_path_base: str | None) -> Model_onnx:
    """Convert TensorFlow model to ONNX

    Parameters
    ----------
    model : Model_tf
        TensorFlow model instance to convert
    onnx_path_base : str | None
        Path to save the converted ONNX model instance to, or None. If set to
        None, ONNX model is not saved

    Returns
    -------
    Model_onnx
        The converted ONNX model instance

    Notes
    -----
    This solution is based on:
        https://github.com/onnx/tensorflow-onnx?tab=readme-ov-file#python-api-reference
    """

    result_, _ = convert_tf_to_onnx(model)
    if onnx_path_base is not None:
        onnx_save(result_, f'{onnx_path_base}.onnx')
    return result_


def torch_to_onnx_(model: Model_torch, shape: Iterable | None,
                   dtype: torch_dtype | str | None,
                   onnx_path_base: str | None,
                   delete_tmp_file: bool = True) -> Model_onnx:
    """Convert PyTorch model to ONNX

    Parameters
    ----------
    model : Model_torch
        PyTorch model instance to convert
    shape : Iterable | None
        Input shape for the given model, must be set only if given model is not
        a ScriptFunction or ScriptModel
    dtype : torch_dtype | str | None
        Input data type for given model, used only if given model is not a
        ScriptFunction or ScriptModel, if set to None torch.float32 is used
    onnx_path_base : str | None
        Path to save the converted ONNX model instance to, or None. If set to
        None, ONNX model is not saved
    delete_tmp_file : bool, optional
        Whether to delete temporarily created ONNX file or not, by default True

    Returns
    -------
    Model_onnx
        The converted ONNX model instance

    Raises
    ------
    RuntimeError
        When the given model is not a ScriptFunction or ScriptModel and shape is
        set to None.

    Notes
    -----
        https://pytorch.org/docs/stable/onnx_torchscript.html#torch.onnx.export
    """

    TMP_FILE_NAME_ = 'model.tmp'
    args_ = ()
    if shape is None:
        if not isinstance(model, (torch_ScriptFunction, torch_ScriptModule)):
            raise RuntimeError('PyTorch models require input shape if they are not script models.')
    else:
        dtype_ = torch_float32 if dtype is None else dtype
        args_ = torch_randn(shape, dtype=dtype_, requires_grad=True)
    torch_onnx_export(model, args_, TMP_FILE_NAME_, export_params=True,
                      opset_version=10, do_constant_folding=True,
                      input_names = ['input'], output_names = ['output'],
                      dynamic_axes={'input' : {0 : 'batch_size'},
                                    'output' : {0 : 'batch_size'}})
    result_ = onnx_load(TMP_FILE_NAME_)
    if delete_tmp_file:
        __remove_file(TMP_FILE_NAME_)
    if onnx_path_base is not None:
        onnx_save(result_, f'{onnx_path_base}.onnx')
    return result_


def __remove_directory(directory_path : str):
    """Remove (non-empty) directory

    Parameters
    ----------
    directory_path : str
        Name or path of the directory to remove
    """
    
    rmtree(directory_path, True)


def __remove_file(file_path : str) -> bool:
    """Remove file

    Parameters
    ----------
    file_path : str
        Name or path of the file to remove

    Returns
    -------
    bool
        Whether the removal was successful or not
    """

    try:
        os_remove(file_path)
        result_ = True
    except OSError:
        result_ = False
    return result_