from ..class_list import Class_List
from ..attributes import Attributes
from abc import abstractmethod

class Element:
    __slots__ = ("__children", "__attributes","__name", "__class_list")
    def __init__(self, __name: str, *children, **attributes):
        """Base Element Class"""
        self.__children = list(children)
        self.__attributes = Attributes(attributes.items())
        self.__name = __name
        self.__class_list = Class_List()

    @abstractmethod
    def __pack__(self):
        return NotImplemented
    
    @property
    def children(self):
        return self.__children

    @property
    def attributes(self):
        return self.__attributes
    
    @property
    def name(self):
        return self.__name
    
    @property
    def class_list(self):
        return self.__class_list