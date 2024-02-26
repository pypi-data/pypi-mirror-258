from .object_base import ObjectBase


class Module(ObjectBase):
    name: str
    members: dict[str, ObjectBase]

    def __init__(self, name: str) -> None:
        self.name = name
        self.members = {}

    def add_member(self, member: ObjectBase, name: str) -> None:
        self.members[name] = member
