from dataclasses import dataclass

from .parameters import Parameters

from ..types import Type, Any


@dataclass
class Signature:
    parameters: Parameters
    return_type: Type = Any
