from .. import typing as t
from ..pack_ import pack

SPACE = " "
NEWLINE = "\n"

def _attributes(attributes):
    for atributo, valor in attributes.items():
        if not valor:
            yield atributo
            continue
        
        if atributo.startswith("_"):
            continue

        if atributo.endswith("_"):
            atributo = atributo[0:-1]
        
        yield f"{atributo}=\"{valor}\""

def _children(children):
    for child in children:
        if isinstance(child, t.Element):
            yield pack(child)
        else:
            yield child

def pack_double(element_name, class_list, children, attributes):
    if class_list:
        attributes["class"] = SPACE.join(class_list)
    def func(attributes, children):
        if attributes == dict():
            element_name1 = element_name + " "
        else:
            element_name1 = element_name

        return f"<{element_name1}{SPACE.join(attributes)}>\n{NEWLINE.join(children)}\n</{element_name}>"
    
    return func(_attributes(attributes), _children(children))

def pack_no_double(element_name, class_list, children, attributes):
    if class_list:
        attributes["class"] = SPACE.join(class_list)
    def func(attributes):
        if attributes == dict():
            element_name1 = element_name + " "
        else:
            element_name1 = element_name

        return f"<{element_name1}{SPACE.join(attributes)}>"
    
    return func(_attributes(attributes))