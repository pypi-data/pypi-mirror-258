from dataclasses import dataclass
from enum import Enum
from typing import Any


from ..types import Type
from ..utils import NO_VALUE


class ParameterKind(Enum):
    POSITIONAL_ONLY = 0
    POSITIONAL_OR_KEYWORD = 1
    VAR_POSITIONAL = 2
    KEYWORD_ONLY = 3
    VAR_KEYWORD = 4


@dataclass(init=False)
class Parameter:
    name: str
    type: Type
    kind: ParameterKind
    default: Any

    def __init__(
        self,
        name: str,
        parameter_type: Type,
        kind: ParameterKind,
        default: Any = NO_VALUE,
    ):
        self.name = name
        self.type = parameter_type
        self.kind = kind
        if default is not NO_VALUE:
            if kind in (ParameterKind.VAR_POSITIONAL, ParameterKind.VAR_KEYWORD):
                raise ValueError("Var args and var kwargs cannot have default values")
            self.default = default

    @property
    def has_default(self) -> bool:
        try:
            return self.default is not NO_VALUE
        except AttributeError:
            return False

    @property
    def is_positional(self) -> bool:
        return self.kind in (
            ParameterKind.POSITIONAL_ONLY,
            ParameterKind.POSITIONAL_OR_KEYWORD,
        )

    @property
    def is_keyword(self) -> bool:
        return self.kind in (
            ParameterKind.KEYWORD_ONLY,
            ParameterKind.POSITIONAL_OR_KEYWORD,
        )

    @property
    def is_var_args(self) -> bool:
        return self.kind is ParameterKind.VAR_POSITIONAL

    @property
    def is_var_kwargs(self) -> bool:
        return self.kind is ParameterKind.VAR_KEYWORD

    @property
    def is_positional_only(self) -> bool:
        return self.kind is ParameterKind.POSITIONAL_ONLY

    @property
    def is_keyword_only(self) -> bool:
        return self.kind is ParameterKind.KEYWORD_ONLY
    
    @property
    def is_positional_or_keyword(self) -> bool:
        return self.kind is ParameterKind.POSITIONAL_OR_KEYWORD

    @classmethod
    def var_args(cls, parameter_type: Type = Any, name="args"):
        return cls(name, parameter_type, ParameterKind.VAR_POSITIONAL)

    @classmethod
    def var_kwargs(cls, parameter_type: Type = Any, name="kwargs"):
        return cls(name, parameter_type, ParameterKind.VAR_KEYWORD)

    @classmethod
    def end_positional(cls):
        return POSITIONAL_END

    @classmethod
    def start_keyword(cls):
        return KEYWORD_START


class _SpecialParameter(Parameter):
    def __init__(self, name: str, kind: ParameterKind):
        super().__init__("", None, kind)


POSITIONAL_END = _SpecialParameter("/", ParameterKind.POSITIONAL_OR_KEYWORD)
KEYWORD_START = _SpecialParameter("*", ParameterKind.VAR_POSITIONAL)
FIRST_PARAMETER = _SpecialParameter("", ParameterKind.POSITIONAL_ONLY)
LAST_PARAMETER = _SpecialParameter("", ParameterKind.VAR_KEYWORD)
