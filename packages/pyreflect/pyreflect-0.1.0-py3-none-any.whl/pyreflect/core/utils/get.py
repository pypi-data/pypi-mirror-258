import inspect

from . import convert

from ..abstract.signature import Signature
from ..python_types import (
    FunctionType,
    ModuleType,
)
from ..types import Type, Any


def function_name(func: FunctionType) -> str:
    return func.__name__


def function_return_type(func: FunctionType) -> Type:
    return inspect.get_annotations(func, eval_str=True).get("return", Any)


def function_signature(func: FunctionType) -> Signature:
    return convert.from_inspect_signature(inspect.signature(func))
    

def module_name(module: ModuleType) -> str:
    return module.__name__


def method_from_bound_method(bound_method: object) -> FunctionType:
    return bound_method.__func__


def instance_from_bound_method(bound_method: object) -> object:
    return bound_method.__self__
