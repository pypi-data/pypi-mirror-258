from .typing import SupportsPack

def pack(Element: SupportsPack) -> str:
    value = Element.__pack__()
    if not isinstance(value, str):
        raise TypeError(f"expected to {type(Element).__name__}.__pack__() to return str "
                        f"object, not {type(value).__name__}")
    
    return value