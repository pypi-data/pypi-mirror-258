import functools


from .reflected_object_base import ReflectedObjectBase

from ..python_types import FunctionType
from ..base.function import Function
from ..base.parameter import Parameter
from ..utils import get, convert


class ReflectedFunction(Function, ReflectedObjectBase[FunctionType]):
    def __init__(self, origin: FunctionType):
        ReflectedObjectBase.__init__(self, origin)
        Function.__init__(self, get.function_name(origin), get.function_signature(origin))

    def _update_origin(self):
        annotations = {
            "return": convert.to_type(self.return_type),
            **{param.name: convert.to_type(param.type) for param in self.parameters},
        }
        positionals: list[Parameter] = list(self.args) + list(self.args_or_kwargs)
        defaults = tuple(param.default for param in positionals if param.has_default)
        kw_defaults = {param.name: param.default for param in self.kwargs if param.has_default}

        self.origin.__annotations__ = annotations
        self.origin.__defaults__ = defaults or None
        self.origin.__kwdefaults__ = kw_defaults or None
