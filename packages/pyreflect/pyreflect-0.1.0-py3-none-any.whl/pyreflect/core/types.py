from typing import Any


class Type:
    name: str

    def __init__(self, wrapped: type) -> None:
        self.__wrapped__ = wrapped


def type_wrapper(cls: type) -> Type:
    class _TypeWrapper(cls, Type):
        def __init__(self, *args, **kwargs) -> None:
            cls.__init__(self, *args, **kwargs)
            Type.__init__(self, cls)

        @property
        def name(self) -> str:
            return cls.__name__

    return _TypeWrapper()


Any = type("_Any__Type", (Type,), {"name": property(lambda _: "Any")})(Any)
