import inspect

from .misc import cached

from ..abstract.parameters import Parameters
from ..abstract.signature import Signature
from ..base.parameter import Parameter, ParameterKind
from ..types import Type, Any, type_wrapper
from ..utils import NO_VALUE


def from_inspect_signature(signature: inspect.Signature) -> Signature:

    args, args_or_kwargs, kwargs = [], [], []
    var_args, var_kwargs = None, None

    for name in signature.parameters:
        param = signature.parameters[name]
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            category = args
        elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            category = args_or_kwargs
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            category = kwargs
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            var_args = param
            continue
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            var_kwargs = param
            continue
        else:
            raise ValueError(f"Unsupported parameter kind: {param.kind}")

        category.append(from_inspect_parameter(param))

    parameters = Parameters.empty()
    parameters.args.extend(args)
    parameters.args_or_kwargs.extend(args_or_kwargs)
    parameters.kwargs.extend(kwargs)

    if var_args is not None:
        param = from_inspect_parameter(var_args)
        parameters.set_var_args(param.type, param.name)
    if var_kwargs is not None:
        param = from_inspect_parameter(var_kwargs)
        parameters.set_var_kwargs(param.type, param.name)

    return Signature(
        parameters,
        (
            from_type(signature.return_annotation)
            if signature.return_annotation is not inspect.Parameter.empty
            else Any
        ),
    )


def from_inspect_parameter(param: inspect.Parameter) -> Parameter:
    return Parameter(
        param.name,
        from_type(param.annotation),
        from_inspect_parameter_kind(param.kind),
        param.default if param.default is not inspect.Parameter.empty else NO_VALUE,
    )


def from_inspect_parameter_kind(kind) -> ParameterKind:
    if kind == inspect.Parameter.POSITIONAL_ONLY:
        return ParameterKind.POSITIONAL_ONLY
    if kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
        return ParameterKind.POSITIONAL_OR_KEYWORD
    if kind == inspect.Parameter.VAR_POSITIONAL:
        return ParameterKind.VAR_POSITIONAL
    if kind == inspect.Parameter.KEYWORD_ONLY:
        return ParameterKind.KEYWORD_ONLY
    if kind == inspect.Parameter.VAR_KEYWORD:
        return ParameterKind.VAR_KEYWORD
    raise ValueError(f"Unknown parameter kind: {kind}")


@cached(exclude=[inspect.Parameter.empty])
def from_type(type_: type) -> Type:
    return Any if type_ is inspect.Parameter.empty else type_wrapper(type_)


def to_type(type_: Type) -> type:
    return type_.__wrapped__
