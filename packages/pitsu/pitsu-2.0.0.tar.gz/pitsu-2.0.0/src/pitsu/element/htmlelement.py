from ..typing import Child
from .element import Element

class HtmlElement(Element):
    def __init__(self, *children: Child, **attributes: str):
        super().__init__("html", *children, **attributes)
    
    def __pack__(self) -> str:
        return "<!DOCTYPE html>\n" + super().__pack__()