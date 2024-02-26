from .parameters import Parameters, ParametersCategory

from ..types import Type, Any
from ..utils import NO_VALUE


class SubBuilder:
    def __init__(self, category: ParametersCategory, builder: "ParametersBuilder"):
        self._category = category
        self._builder = builder

    def add(self, name: str, parameter_type: Type = Any, default: object = NO_VALUE):
        self._category.add(name, parameter_type, default)
        return self

    def end(self):
        return self._builder


class ParametersBuilder:
    def __init__(self):
        self.reset()

    def positional_only(self):
        return SubBuilder(self._parameters.args, self)

    def positional_or_keyword(self):
        return SubBuilder(self._parameters.args_or_kwargs, self)

    def keyword_only(self):
        return SubBuilder(self._parameters.kwargs, self)

    def var_args(self, parameter_type: Type = Any, name="args"):
        if parameter_type is None:
            self._parameters.unset_var_args()
        else:
            self._parameters.set_var_args(parameter_type, name)
        return self

    def var_kwargs(self, parameter_type: Type = Any, name="kwargs"):
        if parameter_type is None:
            self._parameters.unset_var_kwargs()
        else:
            self._parameters.set_var_kwargs(parameter_type, name)
        return self

    def build(self) -> Parameters:
        result = self._parameters
        self.reset()
        return result

    def reset(self):
        self._parameters = Parameters.empty()
        self._category = self._parameters.args
        return self
