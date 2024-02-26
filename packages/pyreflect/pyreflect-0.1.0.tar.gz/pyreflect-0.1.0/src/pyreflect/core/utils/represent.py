from ..base.object_base import ObjectBase
from ..abstract.signature import Signature
from ..types import Type
from ..base.function import Function


def signature_as_string(sig: Signature):
    params = []
    previous = None
    for parameter in sig.parameters:
        name = parameter.name
        if (
            (
                parameter.is_positional_or_keyword
                or parameter.is_keyword_only
                or parameter.is_var_kwargs
            )
            and previous is not None
            and previous.is_positional_only
        ):
            params.append("/")
        elif (
            parameter.is_keyword_only
            and not sig.parameters.var_args
            and previous is not None
            and (previous.is_positional_or_keyword or previous.is_positional_only)
        ):
            params.append("*")
        if parameter.is_var_args:
            name = f"*{name}"
        elif parameter.is_var_kwargs:
            name = f"**{name}"

        if parameter.type is not None:
            name = f"{name}: {type_as_string(parameter.type)}"
            if parameter.has_default:
                name = f"{name} = {parameter.default}"
        params.append(name)
        previous = parameter
    
    return ", ".join(params)


def function_as_string(fn: Function):
    return f"def {fn.name}({signature_as_string(fn.signature)}) -> {type_as_string(fn.return_type)}: ..."


def type_as_string(t: Type):
    return t.name


def object_as_string(obj: ObjectBase):
    if isinstance(obj, Signature):
        return signature_as_string(obj)
    if isinstance(obj, Function):
        return function_as_string(obj)
    if isinstance(obj, Type):
        return type_as_string(obj)
    raise ValueError(f"Unsupported object: {obj}")
