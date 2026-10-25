<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python Encapsulation</h1>
</div>

[<< Previous: Python Polymorphism](./09_python_polymorphism.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Inner Classes >>](./11_python_inner_classes.md)

---

- [📘 Day 21 - Python Encapsulation](#-day-21---python-encapsulation)
  - [What is Encapsulation?](#what-is-encapsulation)
  - [Access Modifiers in Python](#access-modifiers-in-python)
    - [1. Public Members](#1-public-members)
    - [2. Protected Members (Single Leading Underscore `_`)](#2-protected-members-single-leading-underscore-_)
    - [3. Private Members (Double Leading Underscore `__`)](#3-private-members-double-leading-underscore-__)
  - [Understanding Name Mangling](#understanding-name-mangling)
  - [The Python Philosophy: "Consenting Adults"](#the-python-philosophy-consenting-adults)
  - [Encapsulation in Action: A Secure Bank Account](#encapsulation-in-action-a-secure-bank-account)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python Encapsulation

## What is Encapsulation?

**Encapsulation** is one of the fundamental concepts in object-oriented programming. It refers to:
1. **Bundling** data (attributes) and methods that operate on that data into a single unit (a class).
2. **Restricting direct access** to an object's internal components to prevent unauthorized manipulation and maintain internal consistency.

---

## Access Modifiers in Python

Unlike languages like Java or C++ which have strict keywords (`public`, `protected`, `private`), Python relies on naming conventions to signal access intent:

| Access Level | Naming Convention | Example | Meaning |
| :--- | :--- | :--- | :--- |
| **Public** | No prefix | `self.name` | Accessible from anywhere (inside and outside the class) |
| **Protected** | Single leading underscore | `self._name` | Internal convention; intended only for class and subclasses |
| **Private** | Double leading underscore | `self.__name` | Name-mangled; inaccessible directly from outside |

---

### 1. Public Members

Public attributes and methods can be accessed freely anywhere:

```py
class Car:
    def __init__(self, brand):
        self.brand = brand  # Public attribute

car = Car("Toyota")
print(car.brand)  # Toyota
car.brand = "Honda"
print(car.brand)  # Honda
```

---

### 2. Protected Members (Single Leading Underscore `_`)

A single leading underscore (`_`) is a **gentlemen's agreement** among Python programmers. It communicates: *"This attribute/method is intended for internal use within this class and its subclasses. Please do not modify it directly from the outside."*

```py
class Account:
    def __init__(self, balance):
        self._balance = balance  # Protected by convention

    def _internal_audit(self):
        print("Running internal ledger check...")

class SavingsAccount(Account):
    def add_interest(self, rate):
        # Subclasses can safely access protected members
        self._balance += self._balance * rate
```

Python does **not** stop you from accessing `acc._balance`, but linters, IDEs, and other developers will flag it as a code smell.

---

### 3. Private Members (Double Leading Underscore `__`)

When an attribute starts with **two leading underscores** (and no trailing underscores), Python triggers **Name Mangling**.

```py
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary  # Private attribute

emp = Employee("Sarah", 75000)
print(emp.name)       # Sarah

# Trying to access __salary directly will fail:
# print(emp.__salary)
# AttributeError: 'Employee' object has no attribute '__salary'
```

---

## Understanding Name Mangling

Python prevents direct access to `__salary` by automatically prefixing it with `_ClassName`:

```py
# How Python transforms the name internally:
# _<ClassName>__<AttributeName>

print(emp._Employee__salary)  # 75000
```

Name mangling is primarily intended to **prevent accidental name collisions in subclasses**, not to be an unbreakable security barrier.

```py
class Base:
    def __init__(self):
        self.__secret = "Base Secret"

class Sub(Base):
    def __init__(self):
        super().__init__()
        self.__secret = "Sub Secret"

s = Sub()
# s._Base__secret is "Base Secret"
# s._Sub__secret is "Sub Secret"
# No collision occurred between parent and child!
```

---

## The Python Philosophy: "Consenting Adults"

Python community adheres to the famous guideline:

> *"We are all consenting adults here."*

Python trusts developers not to shoot themselves in the foot. Rather than building walls with strict compiler checks, Python uses conventions (`_`), name mangling (`__`), and properties (`@property`) to guide correct access patterns.

---

## Encapsulation in Action: A Secure Bank Account

Here is a complete, well-encapsulated model of a bank account:

```py
class SecureBankAccount:
    def __init__(self, owner: str, initial_balance: float, pin: str):
        self.owner = owner
        self.__balance = float(initial_balance)
        self.__pin = pin
        self._transaction_history = []

    def __verify_pin(self, entered_pin: str) -> bool:
        """Private helper method for internal verification"""
        return self.__pin == entered_pin

    def check_balance(self, pin: str):
        if self.__verify_pin(pin):
            return self.__balance
        raise PermissionError("Invalid PIN!")

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += amount
        self._transaction_history.append(f"+${amount:.2f}")
        return self.__balance

    def withdraw(self, amount: float, pin: str):
        if not self.__verify_pin(pin):
            raise PermissionError("Invalid PIN!")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance!")

        self.__balance -= amount
        self._transaction_history.append(f"-${amount:.2f}")
        return self.__balance

# Testing encapsulated account
acc = SecureBankAccount("Alice", 1000.0, "4321")

acc.deposit(250.0)
print(f"Alice's verified balance: ${acc.check_balance('4321'):.2f}")  # $1250.00

acc.withdraw(100.0, "4321")
print(f"Alice's verified balance: ${acc.check_balance('4321'):.2f}")  # $1150.00

try:
    acc.withdraw(50, "0000")  # Wrong PIN
except PermissionError as e:
    print(f"Denied: {e}")
```

---

## Exercises

1. Create a `User` class with a public `username` and a private `__password_hash`. Provide a method `verify_password(input_password)`.
2. Implement a `Smartphone` class where the battery level (`__battery_percentage`) is private and only modified through `use_phone(minutes)` and `charge(minutes)`. Ensure battery never exceeds 100 or drops below 0.
3. Inspect `dir(Smartphone)` to observe how Python mangled the private attribute name.

---

[<< Previous: Python Polymorphism](./09_python_polymorphism.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Inner Classes >>](./11_python_inner_classes.md)
