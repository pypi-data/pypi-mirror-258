In the project create a file called `main.py` with the following contents:

```python
#main.py
def hello():
    print("Hello")
```

In the same directory, create a file called `__init__.py` with the following content:
```
#__init__.py
from .main import hello
```
