# NeuralBridge

Easy-to-use, one-liner AI model conversion tool between AI frameworks to ensure faster model development and portability with Open Neural Network Exchange (ONNX).

## How to Install

To install NeuralBridge simple use:

` pip install neuralbridge `

In case you would like to build this project from source please consult the ` requirements.txt ` file and the ` src ` directory.

## How to Use

The main use case of NeuralBridge is to convert model runtime. It converts TensorFlow and PyTorch models from one framework to another absolutely automatically. You can access runtime conversion like this:

```Python
from neuralbridge import convert_model

model_in_other_framework = convert_model(model_in_one_framework)
```

## Examples

You can find additional examples in the ` examples ` directory.

### Converting PyTorch model into TensorFlow

This example is in the ` example_tf_to_torch.py ` file.

### Converting TensorFlow model into PyTorch

This example is in the ` example_torch_to_tf.py ` file.

### Old design patterns

You can find the old design patterns in the following files:

- ` old_way_onnx_to_tf.py `

- ` old_way_onnx_to_torch.py `

- ` old_way_tf_to_onnx.py `

- ` old_way_tf_to_torch.py `

- ` old_way_torch_to_onnx.py `

- ` old_way_torch_to_tf.py `

## Requirements

The list of all requirements are in the [requirements.txt](https://gitlab.com/neuralbridge/neuralbridge-python/-/blob/main/requirements.txt).

## License

See details in the [LICENSE](https://gitlab.com/neuralbridge/neuralbridge-python/-/blob/main/LICENSE).