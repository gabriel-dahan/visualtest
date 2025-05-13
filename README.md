# VisualTest

### Install and Import the module :

Installing the module :
```bash
~ git clone https://github.com/gabriel-dahan/visualtest/
~ cd visualtest/

# Linux / MacOS
~ python3 -m pip install -U .

# Windows 
~ py -3 -m pip install -U .
```
_Consider using the `--user` parameter if you're not a root/admin user._

Importing the module :
```python
from visualtest import VisualTest
...
```

### Use the 'VisualTest' class.

Once the class is imported, you can use it by passing a callable as parameter.
```python
def foo(x: str, y: int):
    print(f'1st param : {x}\n2nd param : {y}')

vt = VisualTest(foo)
vt.run()
```
The output will look like this :
```bash
~ #1 x [str] : ...
~ #2 y [int] : ...
```

Here, `x` is the parameter's name and `[str]` its type.

If a parameter has no defined type, `[]` is shown instead, and the user can change the default type (`str`) to `int, float, bool, list, tuple` with `--type <type>`