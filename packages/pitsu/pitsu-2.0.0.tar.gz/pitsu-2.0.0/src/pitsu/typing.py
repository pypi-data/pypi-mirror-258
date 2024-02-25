from typing import *
from typing import __all__ as typing_all
from abc import abstractmethod as _absmethod
from .element.base import Element
from .attributes import Attributes
from .class_list import Class_List

Child = Union[Element, str]
Children = List[Child]

@runtime_checkable
class SupportsPack(Protocol):
    """An ABC with one abstract method __pack__."""
    @_absmethod
    def __pack__(self) -> str: ...

__all__ = [
    "SupportsPack",
    "Child",
    "Children",
    "Attributes",
    "Class_List"
]

__all__.extend(typing_all)
del typing_all