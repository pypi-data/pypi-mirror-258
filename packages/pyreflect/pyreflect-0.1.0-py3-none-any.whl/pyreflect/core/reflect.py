from typing import overload, Callable


from .reflected.reflected_function import ReflectedFunction
from .python_types import (
    # BoundMethodType,
    # ClassType,
    FunctionType,
    # MethodType,
    # ModuleType,
)
from .types import Type
from .utils.reflect import reflect_object


@overload
def reflect(typ: type) -> Type: ...
# @overload
# def reflect(cls: ClassType) -> ReflectedClass: ...
@overload
def reflect(func: Callable) -> ReflectedFunction: ...
@overload
def reflect(func: FunctionType) -> ReflectedFunction: ...
# @overload
# def reflect(method: MethodType) -> ReflectedMethod: ...
# @overload
# def reflect(bound_method: BoundMethodType) -> ReflectedBoundMethod: ...
# @overload
# def reflect(module: ModuleType) -> ReflectedModule: ...

def reflect(obj):
    return reflect_object(obj)
