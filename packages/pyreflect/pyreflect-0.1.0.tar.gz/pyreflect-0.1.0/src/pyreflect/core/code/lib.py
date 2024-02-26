from enum import Enum
from types import ModuleType

from .code_object import CodeObject
from .disassembly import DisassemblyResult


code_lib: "_CodeLibType | None" = None


_EXISTS = lambda lib, feature_name: hasattr(lib, feature_name)
_FUNCTION = lambda lib, feature_name: callable(getattr(lib, feature_name, None))


class UnsupportedFeatureError(NotImplementedError):
    pass


class _CodeLibType(ModuleType):
    def compile(self, code: CodeObject, *args, **kwargs): ...
    def decompile(self, code) -> CodeObject: ...
    def disassemble(self, code) -> DisassemblyResult: ...
    def update_code_object(self, code, new_code): ...


def _name(obj):
    return getattr(obj, "__name__")


class CodeLibFeature(Enum):
    Compile = (_name(_CodeLibType.compile), _FUNCTION)
    Decompile = (_name(_CodeLibType.decompile), _FUNCTION)
    Disassemble = (_name(_CodeLibType.disassemble), _FUNCTION)
    UpdateCodeObject = (_name(_CodeLibType.update_code_object), _FUNCTION)


_FEATURES: dict[CodeLibFeature] = {feature: False for feature in CodeLibFeature}


def _reset_features():
    _FEATURES.clear()

    for feature in CodeLibFeature:
        _FEATURES[feature] = False


def _check_code_lib_features():
    for feature in CodeLibFeature:
        feature_name, check = feature.value
        _FEATURES[feature] = check(code_lib, feature_name)


def supports(feature: CodeLibFeature) -> bool:
    return _FEATURES[feature]


def assert_supports(feature: CodeLibFeature):
    if not supports(feature):
        raise UnsupportedFeatureError(f"Feature {feature.name} is not supported by the code library {code_lib.__name__}")


def is_supported() -> bool:
    return code_lib is not None


def load(reload: bool = False):
    global code_lib

    if code_lib is None or reload:
        _reset_features()

        try:
            import pyreflect.code as code_lib
        except ImportError:
            code_lib = None
        else:
            _check_code_lib_features()


__all__ = [
    "CodeLibFeature",
    "supports",
    "is_supported",
    "load",
    "code_lib",
]
