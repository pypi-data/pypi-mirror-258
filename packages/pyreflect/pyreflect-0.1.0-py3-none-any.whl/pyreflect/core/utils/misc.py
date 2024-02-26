from functools import wraps
from typing import Iterable

from .. import cache


_EMPTY = ()


def cached(func_or_nothing=None, *, exclude: Iterable[object] | None = None):
    if exclude is None:
        exclude = _EMPTY

    def _decorator(func):
        @wraps(func)
        def wrapper(value, *args, enable_caching: bool = True, **kwargs):
            if not enable_caching or value in exclude:
                return func(value, *args, **kwargs)
            try:
                return cache.cache(value)
            except cache.CacheMiss:
                return cache.cache(value, func(value, *args, **kwargs))

        return wrapper

    if callable(func_or_nothing):
        return _decorator(func_or_nothing)
    return _decorator
