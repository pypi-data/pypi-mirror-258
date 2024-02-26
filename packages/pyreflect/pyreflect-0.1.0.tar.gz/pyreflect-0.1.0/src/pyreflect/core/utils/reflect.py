import inspect

from typing import Any


from ..python_types import FunctionType
from ..reflected.reflected_function import ReflectedFunction
from ..types import Type
from ..utils import convert, check


def reflect_object(obj: object) -> Any:
    if check.is_unbound_method(obj):
        return reflect_function(obj)
    if check.is_bound_method(obj):
        return reflect_bound_method(obj)
    if inspect.isclass(obj):
        return reflect_type(obj)
    raise NotImplementedError(f"Cannot reflect object of type {type(obj)}")


def reflect_function(func: FunctionType) -> ReflectedFunction:
    return ReflectedFunction(func)


def reflect_bound_method(bound_method: object) -> ReflectedFunction:
    return ReflectedBoundMethod(bound_method)


def reflect_type(typ: type) -> Type:
    return convert.from_type(typ)
