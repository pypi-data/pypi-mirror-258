from .reflected_object_base import ReflectedObjectBase, ReadOnlyDefault

from ..python_types import ModuleType
from ..base.module import Module

from ..utils import get


class ReflectedModule(Module, ReflectedObjectBase[ModuleType]):
    def __init__(self, origin: ModuleType, readonly: bool = ReadOnlyDefault):
        Module.__init__(self, get.module_name(origin))
        ReflectedObjectBase.__init__(self, origin, readonly)

    def _update_origin(self):
        return super()._update_origin()
