import typing as t

_KT, _VT = (t.TypeVar("_KT"), t.TypeVar("_VT"))

class Attributes(dict[_KT, _VT]):
    def __init__(self, map: t.Iterable[tuple[_KT, _VT]]):
        """Attributes Class"""
        dict.__init__(self, map)
    
    def keys(self) -> t.KeysView[_KT]:
        return t.KeysView(self)
    
    def values(self) -> t.ValuesView[_VT]:
        return t.ValuesView(self)
    
    def items(self) -> t.ItemsView[_KT, _VT]:
        return t.ItemsView(self)