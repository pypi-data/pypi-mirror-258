NoValue = type("NoValue", (), {
    "__repr__": lambda _: "<NO_VALUE>",
    "__bool__": lambda _: False,
    "__eq__": lambda _, other: other is NO_VALUE,
    "__ne__": lambda _, other: other is not NO_VALUE,
    "__hash__": lambda _: 0,
    "__copy__": lambda _: NO_VALUE,
    "__call__": classmethod(lambda cls: NO_VALUE if hasattr(cls, "__instance__") else cls.__new__(cls)),
})
NoValue.__instance__ = NO_VALUE = NoValue()


def evaluate_type_annotation_string(
    annotation: str, _globals: dict, _locals: dict | None = None
) -> type:
    """
    Evaluate a type annotation string and return the resulting type.

    :param annotation: The type annotation string to evaluate.
    :param _globals: The globals dictionary to use when evaluating the type annotation.
    :param _locals: The locals dictionary to use when evaluating the type annotation.
    :return: The resulting type.
    """

    # pylint: disable=eval-used
    return eval(annotation, _globals, _locals)
