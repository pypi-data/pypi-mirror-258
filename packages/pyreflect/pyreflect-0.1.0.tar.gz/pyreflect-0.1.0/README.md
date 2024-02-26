# PyReflect

This library is a simple reflection library for Python. It is designed to be simple and easy to use.


## Installation

```bash
pip install pyreflect
```

## Usage

```python
from pyreflect import reflect


def foo():
    return 1


foo_meta = reflect(foo)
print(foo_meta.name)  # foo
foo_meta.args.add("a", reflect(int))

foo_meta.update_origin()

try:
    foo()
except TypeError as e:
    print(e)  # foo() missing 1 required positional argument: 'a'
