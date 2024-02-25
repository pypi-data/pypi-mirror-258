from . import base
from ..attributes import Attributes
from ..typing import Child, Children
from ..util import pack_helper as ph

class Element(base.Element):
    def __init__(self, __name: str, *children: Child, **attributes: str):
        """Element Class"""
        self.__double = bool(attributes.pop("__double", True))
        super().__init__(__name, *children, **attributes)
    
    @property
    def attributes(self) -> Attributes[str, str]:
        return super().attributes
    
    @property
    def children(self) -> Children:
        return super().children
    
    def __pack__(self) -> str:
        if self.__double:
            pack = ph.pack_double
        else:
            pack = ph.pack_no_double
        
        return pack(self.name, self.class_list, self.children, self.attributes)