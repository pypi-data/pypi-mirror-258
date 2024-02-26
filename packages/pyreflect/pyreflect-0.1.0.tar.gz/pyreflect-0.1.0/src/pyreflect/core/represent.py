from typing import overload


from .base.function import Function
from .base.object_base import ObjectBase
from .utils.represent import object_as_string



@overload
def represent(func: Function) -> str: ...

def represent(obj: ObjectBase) -> str:
    return object_as_string(obj)
