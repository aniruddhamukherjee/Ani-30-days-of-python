<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python self Parameter</h1>
</div>

[<< Previous: Python __init__ Method](./03_python_init_method.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Class Properties >>](./05_python_class_properties.md)

---

- [📘 Day 21 - Python `self` Parameter](#-day-21---python-self-parameter)
  - [What is the `self` Parameter?](#what-is-the-self-parameter)
  - [Why is `self` Explicit in Python?](#why-is-self-explicit-in-python)
  - [How Python Translates Method Calls](#how-python-translates-method-calls)
  - [Is `self` a Python Keyword?](#is-self-a-python-keyword)
  - [Accessing Instance Attributes with `self`](#accessing-instance-attributes-with-self)
  - [Calling Methods from Other Methods via `self`](#calling-methods-from-other-methods-via-self)
  - [What Happens When `self` is Omitted?](#what-happens-when-self-is-omitted)
  - [Passing `self` to External Functions (Callbacks and Delegations)](#passing-self-to-external-functions-callbacks-and-delegations)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python `self` Parameter

## What is the `self` Parameter?

In Python, `self` represents the **instance of the class**. By passing `self` as the first parameter to methods, Python gives the method access to the attributes and other methods belonging to that specific instance.

```py
class Person:
    def __init__(self, name):
        self.name = name  # Attaching attribute 'name' to the current instance

    def greet(self):
        return f"Hello, my name is {self.name}!"

p1 = Person("Alice")
p2 = Person("Bob")

print(p1.greet())  # Hello, my name is Alice!
print(p2.greet())  # Hello, my name is Bob!
```

---

## Why is `self` Explicit in Python?

In languages like C++ or Java, `this` is implicit and hidden. In Python, `self` is made explicit because of Python's guiding philosophy:

> *"Explicit is better than implicit."* — The Zen of Python (PEP 20)

Explicit `self` ensures:
1. You can immediately distinguish between **local variables** and **instance variables** (`x` vs `self.x`).
2. There is no ambiguity about where a variable comes from.
3. Classes and functions operate under uniform, transparent rules.

---

## How Python Translates Method Calls

When you call a method on an object:

```py
p1.greet()
```

Python automatically converts this under the hood into:

```py
Person.greet(p1)
```

Here is concrete proof:

```py
class Greeter:
    def say_hello(self, target):
        return f"Hello, {target}!"

g = Greeter()

# Standard invocation:
print(g.say_hello("World"))

# Explicit class invocation passing the instance manually:
print(Greeter.say_hello(g, "World"))

# Both outputs are identical: "Hello, World!"
```

---

## Is `self` a Python Keyword?

**No**, `self` is not a reserved keyword in Python. You could technically name it `this`, `me`, or anything else:

```py
class Demo:
    def __init__(this, val):
        this.val = val

    def show(this):
        return this.val

d = Demo(100)
print(d.show())  # 100
```

> [!CAUTION]
> **Always use `self`!** Adhering to PEP 8 standards is strictly expected across the entire Python community. Using anything else confuses linters, IDEs, and other developers.

---

## Accessing Instance Attributes with `self`

`self` acts as the bridge connecting methods to instance data:

```py
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Current balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
            return False
        self.balance -= amount
        print(f"Withdrew {amount}. Remaining balance: {self.balance}")
        return True

acc = BankAccount("Sarah", 100)
acc.deposit(50)     # Deposited 50. Current balance: 150
acc.withdraw(70)    # Withdrew 70. Remaining balance: 80
```

---

## Calling Methods from Other Methods via `self`

You can call one method from another within the same class using `self.method_name()`:

```py
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def summary(self):
        # Calling other methods using self
        return f"Rectangle ({self.width}x{self.height}) -> Area: {self.area()}, Perimeter: {self.perimeter()}"

r = Rectangle(5, 3)
print(r.summary())
# Output: Rectangle (5x3) -> Area: 15, Perimeter: 16
```

---

## What Happens When `self` is Omitted?

If you define a method without `self`:

```py
class Calculator:
    def add(a, b):  # Missing self!
        return a + b

calc = Calculator()
# calc.add(2, 3)
```

Calling `calc.add(2, 3)` raises:
```sh
TypeError: Calculator.add() takes 2 positional arguments but 3 were given
```

Why 3 arguments? Because Python passed `calc` automatically as the first argument, plus `2` and `3`!

---

## Passing `self` to External Functions (Callbacks and Delegations)

You can pass `self` outside the class to allow external functions to interact with the current instance:

```py
def audit_logger(entity):
    print(f"[AUDIT] Inspected entity of type {type(entity).__name__} with ID {getattr(entity, 'id', 'N/A')}")

class Order:
    def __init__(self, order_id, total):
        self.id = order_id
        self.total = total

    def process(self):
        print(f"Processing order {self.id} for ${self.total}")
        audit_logger(self)  # Passing the current instance to an external function

order = Order("ORD-9912", 249.99)
order.process()
```

---

## Exercises

1. Create a `Counter` class with `self.count = 0`. Implement `increment()`, `decrement()`, and `reset()` methods.
2. Inside the `Counter` class, add a method `add_multiple(steps)` that uses a loop to call `self.increment()` repeatedly.
3. Write a snippet demonstrating what error occurs when a method tries to access an attribute without `self.`.

---

[<< Previous: Python __init__ Method](./03_python_init_method.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Class Properties >>](./05_python_class_properties.md)
