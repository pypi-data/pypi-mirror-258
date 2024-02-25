from .typing import Child as _Child
from .element.element import Element
from .element.htmlelement import HtmlElement

def __html(*children: _Child, **attributes: str):
    return HtmlElement(*children, **attributes)

def __double_base(name: str, func_name: str = None):
    def func(*children: _Child, **attributes: str):
        attributes.pop("__double", None)
        return Element(name, *children, __double=True, **attributes)

    func.__name__ = func_name or name

    return func

def __not_double_base(name: str, func_name: str = None):
    def func(**attributes: str):
        attributes.pop("__double", None)
        return Element(name, __double=False, **attributes)

    func.__name__ = func_name or name
    
    return func

html = __html
a = __double_base("a")
abbr = __double_base("abbr")
address = __double_base("address")
area = __double_base("area")
aside = __double_base("aside")
audio = __double_base("audio")
b = __double_base("b")
base = __not_double_base("base")
bdo = __double_base("bdo")
blockquote = __double_base("blockquote")
body = __double_base("body")
br = lambda: "<br>"
button = __double_base("button")
canvas = __double_base("canvas")
caption = __double_base("caption")
cite = __double_base("cite")
command = __not_double_base("command")
code = __double_base("code")
col = __not_double_base("col")
colgroup = __double_base("colgroup")
datagrid = __double_base("datagrid")
datalist = __double_base("datalist")
dd = __double_base("dd")
details = __double_base("details")
dfn = __double_base("dfn")
div = __double_base("div")
dl = __double_base("dl")
dialog = __double_base("dialog")
dt = __double_base("dt")
em = __double_base("em")
embed = __not_double_base("embed")
fieldset = __double_base("fieldset")
figure = __double_base("figure")
figcaption = __double_base("figcaption")
footer = __double_base("footer")
form = __double_base("form")
fieldset = __double_base("fieldset")
h1 = __double_base("h1")
h2 = __double_base("h2")
h3 = __double_base("h3")
h4 = __double_base("h4")
h5 = __double_base("h5")
h6 = __double_base("h6")
header = __double_base("header")
head = __double_base("head")
hgroup = __double_base("hgroup")
hr = lambda: "<hr>"
i = __double_base("i")
iframe = __double_base("iframe")
img = __double_base("img")
input = __not_double_base("input")
inp = __not_double_base("input", "inp")
ins = __double_base("ins")
kbd = __double_base("kbd")
label = __double_base("label")
legend = __double_base("legend")
li = __double_base("li")
link = __not_double_base("link")
main = __double_base("main")
map = __double_base("map")
marquee = __double_base("marquee")
menu = __double_base("menu")
meta = __not_double_base("meta")
nav = __double_base("nav")
noscript = __double_base("noscript")
object = __double_base("object")
ol = __double_base("ol")
option = __double_base("option")
optgroup = __double_base("optgroup")
output = __double_base("output")
p = __double_base("p")
param = __not_double_base("param")
picture = __double_base("picture")
pre = __double_base("pre")
progress = __double_base("progress")
q = __double_base("q")
s = __double_base("s")
samp = __double_base("samp")
script = __double_base("script")
section = __double_base("section")
small = __double_base("small")
source = __not_double_base("source")
strong = __double_base("strong")
style = __double_base("style")
sub = __double_base("sub")
summary = __double_base("summary")
sup = __double_base("sup")
table = __double_base("table")
textarea = __double_base("textarea")
tbody = __double_base("tbody")
td = __double_base("td")
tfoot = __double_base("tfoot")
th = __double_base("th")
thead = __double_base("thead")
title = __double_base("title")
tr = __double_base("tr")
u = __double_base("u")
ul = __double_base("ul")
var = __double_base("var")
video = __double_base("video")

br.__name__ = "br"
hr.__name__ = "hr"
html.__name__ = "html"

__all__ = [_item for _item in globals() if not _item.startswith("_")]