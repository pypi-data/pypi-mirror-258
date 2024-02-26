from typing import Generic, TypeVar


T = TypeVar("T")

ReadOnlyDefault = False


class ReflectedObjectBase(Generic[T]):
    _origin: T

    def __init__(self, origin: T, readonly: bool = ReadOnlyDefault):
        self._origin = origin
        self._readonly = readonly

    @property
    def origin(self) -> T:
        return self._origin

    @property
    def readonly(self) -> bool:
        return self._readonly

    def update_origin(self):
        if self._readonly:
            raise ValueError("Object is readonly")
        self._update_origin()

    def _update_origin(self):
        raise NotImplementedError
