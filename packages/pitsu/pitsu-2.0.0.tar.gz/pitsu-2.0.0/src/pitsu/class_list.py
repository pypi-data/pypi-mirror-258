from .errors import ClassError

class Class_List(set[str]):
    def __init__(self):
        """Class_List class"""
        return super().__init__()

    def append(self, obj: str):
        if not isinstance(obj, str):
            raise ClassError(f"expected str, not {type(obj).__name__}")

        super().add(obj)
    
    add = append
    
    def remove(self, obj: str):
        if not isinstance(obj, str):
            raise ClassError(f"expected str, not {type(obj).__name__}")
        
        if not obj in self:
            raise ClassError(f"object {obj} not in Class_List")

        super().remove(obj)