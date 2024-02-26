from typing import Iterable, SupportsIndex


from ..base.parameter import Parameter, ParameterKind
from ..types import Type
from ..utils import NO_VALUE


class ParametersCategory:
    def __init__(self, parameters: Iterable[Parameter], kind: ParameterKind):
        parameters = list(parameters)
        if not all(param.kind == kind for param in parameters):
            raise ValueError("All parameters must have the same kind")

        self._parameters = parameters
        self._kind = kind

    @property
    def parameters(self) -> list[Parameter]:
        return self._parameters.copy()

    @property
    def kind(self) -> ParameterKind:
        return self._kind

    def add(self, name: str, parameter_type: Type, default: object = NO_VALUE) -> None:
        self._parameters.append(Parameter(name, parameter_type, self.kind, default))

    def add_at(self, index: int, name: str, parameter_type: Type, default: object = NO_VALUE) -> None:
        self._parameters.insert(index, Parameter(name, parameter_type, self.kind, default))

    def append(self, parameter: Parameter) -> None:
        if parameter.kind != self.kind:
            raise ValueError("Parameter kind does not match category kind")
        self._parameters.append(parameter)

    def extend(self, parameters: Iterable[Parameter]) -> None:
        for parameter in parameters:
            self.append(parameter)

    def insert(self, index: int, parameter: Parameter) -> None:
        if parameter.kind != self.kind:
            raise ValueError("Parameter kind does not match category kind")
        self._parameters.insert(index, parameter)

    def index(self, parameter: Parameter | str) -> int:
        if isinstance(parameter, str):
            for i, param in enumerate(self._parameters):
                if param.name == parameter:
                    return i
            raise ValueError(f"Parameter not found: {parameter}")
        return self._parameters.index(parameter)

    def find(self, name: str) -> Parameter:
        for parameter in self._parameters:
            if parameter.name == name:
                return parameter
        raise ValueError(f"Parameter not found: {name}")

    def __getitem__(self, index: SupportsIndex | str) -> Parameter:
        if isinstance(index, str):
            return self.find(index)
        return self._parameters[index]

    def __setitem__(self, index: SupportsIndex | str, parameter: Parameter) -> None:
        if parameter.kind != self.kind:
            raise ValueError("Parameter kind does not match category kind")
        if isinstance(index, str):
            index = self.index(index)
        self._parameters[index] = parameter

    def __delitem__(self, index: SupportsIndex | str) -> None:
        if isinstance(index, str):
            index = self.index(index)
        del self._parameters[index]

    def __contains__(self, parameter: Parameter | str) -> bool:
        if isinstance(parameter, str):
            try:
                self.index(parameter)
                return True
            except ValueError:
                return False
        return parameter in self._parameters

    def __len__(self) -> int:
        return len(self._parameters)

    def __iter__(self) -> Iterable[Parameter]:
        return iter(self._parameters)


class Parameters:
    _args: ParametersCategory
    _args_or_kwargs: ParametersCategory
    _kwargs: ParametersCategory
    _var_args: Parameter | None
    _var_kwargs: Parameter | None

    def __init__(
        self,
        args: Iterable[Parameter],
        args_or_kwargs: Iterable[Parameter],
        kwargs: Iterable[Parameter],
        var_args: Parameter | None = None,
        var_kwargs: Parameter | None = None,
    ):
        self._args = ParametersCategory(args, ParameterKind.POSITIONAL_ONLY)
        self._args_or_kwargs = ParametersCategory(args_or_kwargs, ParameterKind.POSITIONAL_OR_KEYWORD)
        self._kwargs = ParametersCategory(kwargs, ParameterKind.KEYWORD_ONLY)
        self._var_args = var_args
        self._var_kwargs = var_kwargs
        self._parameters: list[Parameter] | None = None

    @property
    def args(self) -> ParametersCategory:
        return self._args

    @property
    def args_or_kwargs(self) -> ParametersCategory:
        return self._args_or_kwargs

    @property
    def kwargs(self) -> ParametersCategory:
        return self._kwargs

    @property
    def var_args(self) -> Parameter | None:
        return self._var_args

    @property
    def var_kwargs(self) -> Parameter | None:
        return self._var_kwargs

    @property
    def parameters(self) -> list[Parameter]:
        if self._should_recalculate_parameters():
            self._parameters = list(self._args.parameters) + list(self._args_or_kwargs.parameters)
            if self._var_args is not None:
                self._parameters.append(self._var_args)
            self._parameters.extend(self._kwargs.parameters)
            if self._var_kwargs is not None:
                self._parameters.append(self._var_kwargs)
        assert self._parameters is not None
        return self._parameters

    def set_var_args(self, parameter_type: Type, name: str = "args") -> None:
        self._var_args = Parameter(name, parameter_type, ParameterKind.VAR_POSITIONAL)

    def set_var_kwargs(self, parameter_type: Type, name: str = "kwargs") -> None:
        self._var_kwargs = Parameter(name, parameter_type, ParameterKind.VAR_KEYWORD)

    def unset_var_args(self) -> None:
        self._var_args = None

    def unset_var_kwargs(self) -> None:
        self._var_kwargs = None

    def index(self, parameter: Parameter | str) -> int:
        if isinstance(parameter, str):
            for i, param in enumerate(self.parameters):
                if param.name == parameter:
                    return i
            raise ValueError(f"Parameter not found: {parameter}")
        return self.parameters.index(parameter)

    def __getitem__(self, index: SupportsIndex | str) -> Parameter:
        if isinstance(index, SupportsIndex):
            return self.parameters[index]
        elif isinstance(index, str):
            for parameter in self.parameters:
                if parameter.name == index:
                    return parameter
            raise KeyError(f"Parameter not found: {index}")
        raise TypeError(f"Invalid index type: {type(index)}")

    def __contains__(self, parameter: Parameter | str) -> bool:
        if isinstance(parameter, str):
            try:
                self.index(parameter)
                return True
            except ValueError:
                return False
        return parameter in self.parameters

    def __len__(self) -> int:
        return len(self.parameters)

    def __iter__(self):
        return iter(self.parameters)

    def invalidate(self) -> None:
        self._parameters = None

    def _should_recalculate_parameters(self) -> bool:
        if self._parameters is None:
            return True
        length = len(self._args) + len(self._args_or_kwargs) + len(self._kwargs)
        if self._var_args is not None:
            length += 1
        if self._var_kwargs is not None:
            length += 1
        return length != len(self._parameters)

    @classmethod
    def empty(cls):
        return cls((), (), ())
