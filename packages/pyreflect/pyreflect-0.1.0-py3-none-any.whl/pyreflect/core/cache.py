from typing import TypeVar, overload

from .base.object_base import ObjectBase
from .utils import NO_VALUE, NoValue


T = TypeVar("T", bound=ObjectBase)


_CACHE: dict[object, ObjectBase] = {}


class CacheMiss(KeyError):
    def __init__(self, obj: object):
        super().__init__(f"Cache miss for object {obj!r}")


@overload
def cache(obj: object) -> ObjectBase: ...
@overload
def cache(obj: object, reflected: T) -> T: ...

def cache(obj: object, reflected: T = NO_VALUE) -> T | None:
    if reflected is not NO_VALUE:
        _CACHE[obj] = reflected
        return reflected
    try:
        return _CACHE[obj]
    except KeyError as exc:
        raise CacheMiss(obj) from exc


def uncache(obj: object, must_exist: bool = True) -> ObjectBase | NoValue:
    return _CACHE.pop(obj) if must_exist else _CACHE.pop(obj, NO_VALUE)
