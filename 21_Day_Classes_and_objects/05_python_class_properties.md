<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python Class Properties</h1>
</div>

[<< Previous: Python self Parameter](./04_python_self_parameter.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Class Methods >>](./06_python_class_methods.md)

---

- [📘 Day 21 - Python Class Properties](#-day-21---python-class-properties)
  - [What are Class Properties?](#what-are-class-properties)
  - [The Pythonic Way: Why Avoid `get_x()` and `set_x()`](#the-pythonic-way-why-avoid-get_x-and-set_x)
  - [The `@property` Decorator (Getter)](#the-property-decorator-getter)
  - [Adding a Setter (`@<name>.setter`)](#adding-a-setter-namesetter)
  - [Adding a Deleter (`@<name>.deleter`)](#adding-a-deleter-namedeleter)
  - [Read-Only and Computed Properties](#read-only-and-computed-properties)
  - [Class Attributes vs Properties](#class-attributes-vs-properties)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python Class Properties

## What are Class Properties?

In Python, a **property** is a special attribute that allows you to customize access to an underlying instance variable. Properties let you define methods that behave like ordinary attributes, allowing you to intercept reading, writing, and deletion.

---

## The Pythonic Way: Why Avoid `get_x()` and `set_x()`

In languages such as Java or C++, it is standard to write explicit getter and setter methods:

```py
# Non-Pythonic (Java style)
class Person:
    def __init__(self, age):
        self._age = age

    def get_age(self):
        return self._age

    def set_age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self._age = value
```

In Python, this is considered unpythonic. Python provides the `@property` decorator, enabling clean attribute access syntax (`person.age`) while still executing validation logic behind the scenes!

---

## The `@property` Decorator (Getter)

The `@property` decorator turns a method into a read-only getter attribute:

```py
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """Getter for celsius"""
        return self._celsius

t = Temperature(25)
print(t.celsius)  # 25 (accessed like an attribute, not a method call t.celsius())

# Trying to set it raises an AttributeError because no setter is defined yet:
# t.celsius = 30  # AttributeError: can't set attribute 'celsius'
```

---

## Adding a Setter (`@<name>.setter`)

To allow modifying the property while enforcing validation, define a setter using `@<property_name>.setter`:

```py
class Temperature:
    def __init__(self, celsius):
        self._celsius = None
        self.celsius = celsius  # Calls the setter for initial validation

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be a number.")
        if value < -273.15:
            raise ValueError("Temperature below absolute zero (-273.15°C) is impossible!")
        self._celsius = value

t = Temperature(20)
print(t.celsius)  # 20

t.celsius = 35    # Calls the setter cleanly
print(t.celsius)  # 35

try:
    t.celsius = -300  # Raises ValueError
except ValueError as e:
    print(f"Validation Error: {e}")
```

---

## Adding a Deleter (`@<name>.deleter`)

You can define custom behavior when an attribute is deleted with `del`:

```py
class UserAccount:
    def __init__(self, username):
        self._username = username

    @property
    def username(self):
        return self._username

    @username.deleter
    def username(self):
        print(f"Logging deletion of user: {self._username}")
        self._username = None

user = UserAccount("alice99")
print(user.username)  # alice99

del user.username     # Triggers deleter
print(user.username)  # None
```

---

## Read-Only and Computed Properties

Properties are ideal for values dynamically computed from other attributes without storing redundant data:

```py
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        import math
        return math.pi * (self.radius ** 2)

c = Circle(5)
print(f"Radius: {c.radius}")       # 5
print(f"Diameter: {c.diameter}")   # 10
print(f"Area: {c.area:.2f}")       # 78.54

# If radius changes, computed properties update automatically
c.radius = 10
print(f"New Area: {c.area:.2f}")   # 314.16
```

Another classic example: combining `first_name` and `last_name`:

```py
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, name):
        parts = name.split()
        if len(parts) >= 2:
            self.first_name = parts[0]
            self.last_name = " ".join(parts[1:])
        else:
            raise ValueError("Full name must contain first and last name.")

p = Person("Guido", "van Rossum")
print(p.full_name)  # Guido van Rossum

p.full_name = "Tim Peters"
print(p.first_name) # Tim
print(p.last_name)  # Peters
```

---

## Class Attributes vs Properties

| Feature | Class Attribute | Property (`@property`) |
| :--- | :--- | :--- |
| **Location** | Class body | Method decorated with `@property` |
| **Storage** | Stored once in class dict | Dynamic; backed by an instance attribute |
| **Invocation** | Direct lookup (`Obj.attr`) | Method invoked under the hood |
| **Validation** | No built-in validation | Arbitrary validation logic in setter |
| **Computation** | Static value | Can be dynamically recomputed on every access |

---

## Exercises

1. Create a `Product` class with `name` and `price`. Use `@property` to ensure `price` cannot be set to a negative number.
2. Add a read-only property `tax_inclusive_price` that computes the price with a 20% tax applied.
3. Create a `Password` class where the password can be set, but reading the property returns a masked string like `"********"`.

---

[<< Previous: Python self Parameter](./04_python_self_parameter.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Class Methods >>](./06_python_class_methods.md)
