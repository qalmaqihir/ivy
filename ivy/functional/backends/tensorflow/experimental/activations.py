from typing import Optional, Union

# global
import tensorflow as tf
from tensorflow.python.types.core import Tensor

# local
import ivy
from ivy.func_wrapper import with_unsupported_dtypes
from . import backend_version


def logit(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    eps: Optional[float] = None,
    out: Optional[Tensor] = None,
) -> Tensor:
    x_dtype = x.dtype
    if eps is None:
        x = tf.where(tf.math.logical_or(x > 1, x < 0), ivy.nan, x)
    else:
        x = tf.clip_by_value(x, eps, 1 - eps)
    return tf.cast(tf.math.log(x / (1 - x)), x_dtype)


@with_unsupported_dtypes({"2.9.1 and below": ("complex",)}, backend_version)
def thresholded_relu(
    x: Tensor,
    /,
    *,
    threshold: Union[int, float] = 0,
    out: Optional[Tensor] = None,
) -> Tensor:
    return tf.where(x > threshold, x, 0)


@with_unsupported_dtypes({"2.9.1 and below": ("complex",)}, backend_version)
def relu6(x: Tensor, /, *, out: Optional[Tensor] = None) -> Tensor:
    return tf.nn.relu6(x)


def logsigmoid(input: Tensor) -> Tensor:
    return tf.math.log_sigmoid(input)


@with_unsupported_dtypes({"2.9.1 and below": ("bfloat16",)}, backend_version)
def selu(x: Tensor, /, *, out: Optional[Tensor] = None) -> Tensor:
    ret = tf.nn.selu(x)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret).astype(x.dtype)
    return ivy.astype(ret, x.dtype)
