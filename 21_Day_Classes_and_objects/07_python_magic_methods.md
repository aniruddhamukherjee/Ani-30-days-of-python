<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python Magic Methods</h1>
</div>

[<< Previous: Python Class Methods](./06_python_class_methods.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Inheritance >>](./08_python_inheritance.md)

---

- [📘 Day 21 - Python Magic Methods](#-day-21---python-magic-methods)
  - [What are Magic (Dunder) Methods?](#what-are-magic-dunder-methods)
  - [String Representations: `__str__` vs `__repr__`](#string-representations-__str__-vs-__repr__)
  - [Length and Container Methods](#length-and-container-methods)
  - [Operator Overloading](#operator-overloading)
    - [Arithmetic Operators](#arithmetic-operators)
    - [Comparison Operators](#comparison-operators)
  - [Making Objects Callable: `__call__`](#making-objects-callable-__call__)
  - [Context Managers: `__enter__` and `__exit__`](#context-managers-__enter__-and-__exit__)
  - [Comprehensive Example: A 2D Vector Class](#comprehensive-example-a-2d-vector-class)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python Magic Methods

## What are Magic (Dunder) Methods?

**Magic methods** (also called **dunder methods** because they start and end with **d**ouble **under**scores, like `__init__`) are special methods in Python that allow custom classes to hook into Python's built-in operators, protocols, and standard functions.

Whenever you use operations like `+`, `==`, `len()`, or `print()`, Python actually invokes corresponding magic methods behind the scenes.

---

## String Representations: `__str__` vs `__repr__`

Without string representation methods, printing an object outputs an uninformative memory pointer: `<__main__.Book object at 0x000001>`.

Python provides two methods to display objects:
- **`__str__(self)`**: Designed to be **readable**, informal, and user-friendly (invoked by `print(obj)` and `str(obj)`).
- **`__repr__(self)`**: Designed to be **unambiguous**, precise, and intended for developers and debugging (invoked in the Python interactive shell and by `repr(obj)`). Ideally, `eval(repr(obj))` should reconstruct the object.

```py
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

book = Book("1984", "George Orwell", 328)

print(str(book))   # '1984' by George Orwell
print(repr(book))  # Book(title='1984', author='George Orwell', pages=328)
```

---

## Length and Container Methods

You can make your custom class behave like a built-in Python sequence (list, dictionary, tuple) using container dunder methods:

| Method | Built-in trigger | Description |
| :--- | :--- | :--- |
| `__len__(self)` | `len(obj)` | Returns length/item count |
| `__getitem__(self, key)` | `obj[key]` | Accesses an item by index/key |
| `__setitem__(self, key, val)`| `obj[key] = val` | Assigns a value at index/key |
| `__contains__(self, item)` | `item in obj` | Implements membership testing |

```py
class SkillSet:
    def __init__(self):
        self._skills = []

    def add_skill(self, skill):
        self._skills.append(skill)

    def __len__(self):
        return len(self._skills)

    def __getitem__(self, index):
        return self._skills[index]

    def __contains__(self, skill):
        return skill in self._skills

skills = SkillSet()
skills.add_skill("Python")
skills.add_skill("JavaScript")

print(len(skills))         # 2
print(skills[0])           # Python
print("Python" in skills)  # True
print("Go" in skills)      # False
```

---

## Operator Overloading

Operator overloading allows custom objects to define how standard operators (`+`, `-`, `*`, `==`, `<`) work with them.

### Arithmetic Operators

| Operator | Dunder Method | Example |
| :---: | :--- | :--- |
| `+` | `__add__(self, other)` | `a + b` |
| `-` | `__sub__(self, other)` | `a - b` |
| `*` | `__mul__(self, other)` | `a * b` |
| `/` | `__truediv__(self, other)` | `a / b` |
| `//` | `__floordiv__(self, other)` | `a // b` |
| `%` | `__mod__(self, other)` | `a % b` |
| `**` | `__pow__(self, other)` | `a ** b` |

### Comparison Operators

| Operator | Dunder Method | Example |
| :---: | :--- | :--- |
| `==` | `__eq__(self, other)` | `a == b` |
| `!=` | `__ne__(self, other)` | `a != b` |
| `<` | `__lt__(self, other)` | `a < b` |
| `<=` | `__le__(self, other)` | `a <= b` |
| `>` | `__gt__(self, other)` | `a > b` |
| `>=` | `__ge__(self, other)` | `a >= b` |

---

## Making Objects Callable: `__call__`

Defining `__call__` allows an instance to be invoked just like a standard function:

```py
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, number):
        return number * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
print(callable(double))  # True
```

---

## Context Managers: `__enter__` and `__exit__`

You can enable the `with` statement on custom classes by implementing `__enter__` and `__exit__`:

```py
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end = time.time()
        print(f"Elapsed time: {self.end - self.start:.4f} seconds")

# Usage:
with Timer():
    total = sum(i ** 2 for i in range(1000000))
```

---

## Comprehensive Example: A 2D Vector Class

Here is a practical, complete example showing several magic methods working together:

```py
import math

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # String representations
    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    # Vector addition: v1 + v2
    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented

    # Vector subtraction: v1 - v2
    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return NotImplemented

    # Scalar or dot multiplication: v * scalar
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        return NotImplemented

    # Equality check: v1 == v2
    def __eq__(self, other):
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        return False

    # Magnitude: abs(v)
    def __abs__(self):
        return math.hypot(self.x, self.y)

# Testing the Vector2D class
v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print(f"v1 = {v1}")            # (3, 4)
print(f"v1 + v2 = {v1 + v2}")   # (4, 6)
print(f"v1 - v2 = {v1 - v2}")   # (2, 2)
print(f"v1 * 3 = {v1 * 3}")     # (9, 12)
print(f"Magnitude: {abs(v1)}")  # 5.0
print(f"v1 == Vector2D(3, 4): {v1 == Vector2D(3, 4)}")  # True
```

---

## Exercises

1. Create a `Money` class with `amount` and `currency`. Overload `+` and `-` so that adding two money objects with the same currency works, but adding different currencies raises a `ValueError`.
2. Implement `__eq__`, `__lt__`, and `__gt__` on the `Money` class.
3. Implement `__str__` to output `$100.00` and `__repr__` to output `Money(100.00, 'USD')`.

---

[<< Previous: Python Class Methods](./06_python_class_methods.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Inheritance >>](./08_python_inheritance.md)
