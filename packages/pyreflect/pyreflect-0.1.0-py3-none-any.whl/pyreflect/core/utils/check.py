import inspect


def is_unbound_method(obj: object) -> bool:
    return inspect.isfunction(obj)


def is_bound_method(obj: object) -> bool:
    return inspect.ismethod(obj)


def is_static_method(obj: object) -> bool:
    return is_unbound_method(obj) and isinstance(obj, staticmethod)


def is_unbound_class_method(obj: object) -> bool:
    return is_unbound_method(obj) and isinstance(obj, classmethod)


def is_bound_class_method(obj: object) -> bool:
    return is_bound_method(obj) and isinstance(obj.__func__, classmethod)


def is_class_method(obj: object) -> bool:
    return is_unbound_class_method(obj) or is_bound_class_method(obj)
