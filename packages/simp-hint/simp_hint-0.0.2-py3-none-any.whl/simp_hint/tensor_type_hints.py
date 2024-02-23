from typing import Callable, Any, Type, NewType, Type, TypeVar, ParamSpec

import torch

T = TypeVar('T')
P = ParamSpec('P')

def wrap(torch_tensor: Callable[P, Any], tensor_type: Type[T]):
    def make_typed_tensor(*args: P.args, **kwargs: P.kwargs)->T:
        return tensor_type(torch_tensor(*args, **kwargs))
    return make_typed_tensor


FloatTensorHint = NewType('FloatTensorHint', torch.Tensor)
DoubleTensorHint = NewType('DoubleTensorHint', torch.Tensor)
HalfTensorHint = NewType('HalfTensorHint', torch.Tensor)
BFloat16TensorHint = NewType('BFloat16TensorHint', torch.Tensor)
ByteTensorHint = NewType('ByteTensorHint', torch.Tensor)
CharTensorHint = NewType('CharTensorHint', torch.Tensor)
ShortTensorHint = NewType('ShortTensorHint', torch.Tensor)
IntTensorHint = NewType('IntTensorHint', torch.Tensor)
LongTensorHint = NewType('LongTensorHint', torch.Tensor) 
BoolTensorHint = NewType('BoolTensorHint', torch.Tensor) 

float_tensor = wrap(torch.FloatTensor, FloatTensorHint)
half_tensor = wrap(torch.HalfTensor, HalfTensorHint)
bfloat16_tensor = wrap(torch.BFloat16Tensor, BFloat16TensorHint)
byte_tensor = wrap(torch.ByteTensor, ByteTensorHint)
char_tensor = wrap(torch.CharTensor, CharTensorHint)
short_tensor = wrap(torch.ShortTensor, ShortTensorHint)
int_tensor = wrap(torch.IntTensor, IntTensorHint)
long_tensor = wrap(torch.LongTensor, LongTensorHint)
bool_tensor = wrap(torch.BoolTensor, BoolTensorHint)