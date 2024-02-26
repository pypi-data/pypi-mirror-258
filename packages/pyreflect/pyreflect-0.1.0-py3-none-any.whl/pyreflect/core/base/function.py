from ..abstract.parameters import Parameters
from ..abstract.signature import Signature
from ..types import Type


class Function:
    name: str
    signature: Signature

    def __init__(self, name: str, return_type_or_signature: Type | Signature):
        self.name = name
        if isinstance(return_type_or_signature, Type):
            return_type_or_signature = Signature(
                Parameters.empty(), return_type_or_signature
            )
        self.signature = return_type_or_signature

    @property
    def return_type(self) -> Type:
        return self.signature.return_type

    @return_type.setter
    def return_type(self, value: Type):
        self.signature.return_type = value

    @property
    def parameters(self) -> Parameters:
        return self.signature.parameters

    @property
    def var_args(self) -> Type | None:
        var_args = self.signature.parameters.var_args
        if var_args is not None:
            return var_args.type
        return None

    @var_args.setter
    def var_args(self, value: Type | None):
        if value is not None:
            self.signature.parameters.set_var_args(value)
        else:
            self.signature.parameters.unset_var_args()

    @property
    def var_kwargs(self) -> Type | None:
        var_kwargs = self.signature.parameters.var_kwargs
        if var_kwargs is not None:
            return var_kwargs.type
        return None

    @var_kwargs.setter
    def var_kwargs(self, value: Type | None):
        if value is not None:
            self.signature.parameters.set_var_kwargs(value)
        else:
            self.signature.parameters.unset_var_kwargs()

    @property
    def args(self):
        return self.signature.parameters.args

    @property
    def args_or_kwargs(self):
        return self.signature.parameters.args_or_kwargs

    @property
    def kwargs(self):
        return self.signature.parameters.kwargs

    @property
    def is_var_args(self) -> bool:
        return self.var_args is not None

    @property
    def is_var_kwargs(self) -> bool:
        return self.var_kwargs is not None
