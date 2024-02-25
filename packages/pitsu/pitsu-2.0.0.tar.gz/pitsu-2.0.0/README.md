# how to use

* instal pitsu:

```bash
pip3 install pitsu
```

or 

```bash
pip install pitsu
```

simple example:

```python
from pitsu import *

html(
    head(
        meta(charset="UTF-8"),
        title("Example Login")
    ),
    body(
        form(
            inp( # inp = input element
                type="text",
                name="user",
                id="user",
                required=NO_VALUE
            ),
            br(),
            inp(
                type="password",
                name="pass",
                id="pass",
                required=NO_VALUE
            ),
            br(),
            inp(
                type="submit",
                value="Submit"
            ),
            action="/",
            method="get"
        )
    ),
    lang="en"
).pack()
```

you can use the method pack to pack your html page:

```python
page = html(
    ...
)

pack(page)
```

output:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>
Example Login
</title>
</head>
<body>
<form action="/" method="get">
<input type="text" name="user" id="user" required />
<br>
<input type="password" name="pass" id="pass" required />
<br>
<input type="submit" value="Submit" />
</form>
</body>
</html>
```

see <a href="/Docs/main.md">Documentation</a>