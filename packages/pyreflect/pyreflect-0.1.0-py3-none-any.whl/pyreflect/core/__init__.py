from .reflect import reflect
from .represent import represent

__version__ = "0.1.0"


def _init():
    from .code import lib

    lib.load()


_init()
del _init


__all__ = [
    "reflect",
    "represent",
]
