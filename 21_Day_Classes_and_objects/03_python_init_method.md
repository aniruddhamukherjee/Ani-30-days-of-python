<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python __init__ Method</h1>
</div>

[<< Previous: Python Classes & Objects](./02_python_classes_objects.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python self Parameter >>](./04_python_self_parameter.md)

---

- [📘 Day 21 - Python `__init__` Method](#-day-21---python-__init__-method)
  - [What is the `__init__` Method?](#what-is-the-__init__-method)
  - [Syntax and Basic Example](#syntax-and-basic-example)
  - [How Object Creation Works (`__new__` vs `__init__`)](#how-object-creation-works-__new__-vs-__init__)
  - [Constructors with Default Parameter Values](#constructors-with-default-parameter-values)
  - [Using `*args` and `**kwargs` in `__init__`](#using-args-and-kwargs-in-__init__)
  - [Input Validation in `__init__`](#input-validation-in-__init__)
  - [Common Pitfalls and Mistakes](#common-pitfalls-and-mistakes)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python `__init__` Method

## What is the `__init__` Method?

In Python, the `__init__()` method is a special built-in method known as the **initializer** or **constructor**.

When you instantiate a class, Python automatically calls `__init__()` to initialize the newly created object's state by assigning initial values to its instance attributes.

---

## Syntax and Basic Example

```py
class Person:
    def __init__(self, firstname, lastname, age):
        # Initializing instance attributes
        self.firstname = firstname
        self.lastname = lastname
        self.age = age

# Creating an instance triggers __init__ automatically
p = Person("Asabeneh", "Yetayeh", 250)

print(p.firstname)  # Asabeneh
print(p.lastname)   # Yetayeh
print(p.age)        # 250
```

Notice that we passed three arguments (`"Asabeneh"`, `"Yetayeh"`, `250`), but the `__init__` method signature has four parameters: `self`, `firstname`, `lastname`, and `age`. Python automatically supplies the current instance for `self`.

---

## How Object Creation Works (`__new__` vs `__init__`)

In Python, instantiation is a two-step process:
1. **`__new__(cls, ...)`**: Creates and allocates the object in memory. It is the actual constructor that returns a new instance.
2. **`__init__(self, ...)`**: Receives the newly created instance and initializes its attributes. It is the initializer.

```mermaid
flowchart LR
    A["Person('Alice')"] --> B["__new__(cls) - Allocates Object"]
    B --> C["__init__(self) - Sets Attributes"]
    C --> D["Initialized Object Ready"]
```

In 99% of daily programming, you only override `__init__`. You only override `__new__` for advanced metaprogramming or when subclassing immutable types (like `int`, `str`, `tuple`).

---

## Constructors with Default Parameter Values

You can provide default argument values in `__init__`, making parameters optional when creating an instance:

```py
class User:
    def __init__(self, username, email, is_active=True, role="member"):
        self.username = username
        self.email = email
        self.is_active = is_active
        self.role = role

# Using defaults
user1 = User("johndoe", "john@example.com")
print(user1.username, user1.role, user1.is_active)  # johndoe member True

# Overriding defaults
admin = User("admin1", "admin@corp.com", is_active=True, role="administrator")
print(admin.username, admin.role)                   # admin1 administrator
```

> [!WARNING]
> Do not use mutable default arguments (like `def __init__(self, skills=[])`). All instances without an explicit argument would share the **same list**! Instead, use `skills=None` and initialize with `self.skills = skills if skills is not None else []`.

---

## Using `*args` and `**kwargs` in `__init__`

For flexible initialization, you can accept arbitrary positional and keyword arguments:

```py
class Configuration:
    def __init__(self, env, *tags, **settings):
        self.env = env
        self.tags = list(tags)
        self.settings = settings

cfg = Configuration("production", "secure", "v2", debug=False, timeout=30)

print(cfg.env)       # production
print(cfg.tags)      # ['secure', 'v2']
print(cfg.settings)  # {'debug': False, 'timeout': 30}
```

---

## Input Validation in `__init__`

The `__init__` method is the ideal place to guard object invariants and validate input data:

```py
class BankAccount:
    def __init__(self, account_number, initial_balance=0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        if not isinstance(account_number, str) or len(account_number) < 5:
            raise ValueError("Account number must be a string with at least 5 characters.")

        self.account_number = account_number
        self.balance = float(initial_balance)

# Valid account
account = BankAccount("ACC-10023", 500.0)
print(f"Account {account.account_number} created with ${account.balance:.2f}")

# Invalid account raises ValueError
try:
    bad_account = BankAccount("123", -50)
except ValueError as e:
    print(f"Error creating account: {e}")
```

---

## Common Pitfalls and Mistakes

### 1. Returning a Value from `__init__`
`__init__` must always return `None`. Trying to return anything else raises a `TypeError`:
```py
class BadExample:
    def __init__(self):
        return "Hello"  # TypeError: __init__() should return None, not 'str'
```

### 2. Forgetting `self` in the Definition
```py
# INCORRECT:
class Person:
    def __init__(name): # Missing self!
        pass

# Calling Person("Alice") will raise:
# TypeError: Person.__init__() takes 1 positional argument but 2 were given
```

### 3. Forgetting `self.` when Assigning Attributes
```py
class Person:
    def __init__(self, name):
        name = name  # Only creates a local variable! Not attached to self!

p = Person("John")
# print(p.name) -> AttributeError: 'Person' object has no attribute 'name'
```

---

## Exercises

1. Create a `Book` class with an `__init__` method that accepts `title`, `author`, `pages`, and `year`. Provide default values for `pages=0` and `year=None`.
2. Update the `Book` class constructor to raise a `ValueError` if `pages` is negative.
3. Create a `Student` class where `skills` defaults safely to an empty list without sharing mutable state across instances.

---

[<< Previous: Python Classes & Objects](./02_python_classes_objects.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python self Parameter >>](./04_python_self_parameter.md)
