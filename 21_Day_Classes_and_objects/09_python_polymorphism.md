<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python Polymorphism</h1>
</div>

[<< Previous: Python Inheritance](./08_python_inheritance.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Encapsulation >>](./10_python_encapsulation.md)

---

- [📘 Day 21 - Python Polymorphism](#-day-21---python-polymorphism)
  - [What is Polymorphism?](#what-is-polymorphism)
  - [Polymorphism in Built-in Functions and Operators](#polymorphism-in-built-in-functions-and-operators)
  - [Polymorphism with Class Methods](#polymorphism-with-class-methods)
  - [Duck Typing: The Python Way](#duck-typing-the-python-way)
  - [Polymorphism with Inheritance](#polymorphism-with-inheritance)
  - [Abstract Base Classes (ABCs) for Strict Contracts](#abstract-base-classes-abcs-for-strict-contracts)
  - [Real-World Design: Payment Processing Pipeline](#real-world-design-payment-processing-pipeline)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python Polymorphism

## What is Polymorphism?

The word **Polymorphism** is derived from Greek: *poly* (many) and *morph* (form). In programming, polymorphism refers to the ability of different classes or types to respond to the same method call or interface in their own distinct ways.

This allows you to write clean, generic code that works uniformly across diverse objects without caring about their specific underlying class.

---

## Polymorphism in Built-in Functions and Operators

You have been using polymorphism in Python from Day 1!

### 1. The `len()` Function
The built-in `len()` function can determine the length of completely different data types:
```py
print(len("Hello World"))    # 11 (str)
print(len([1, 2, 3, 4]))     # 4  (list)
print(len({"a": 1, "b": 2})) # 2  (dict)
```

### 2. The `+` Operator
The `+` operator performs addition for integers/floats, but concatenation for strings and lists:
```py
print(10 + 20)                 # 30
print("Python" + " Rocks")     # Python Rocks
print([1, 2] + [3, 4])         # [1, 2, 3, 4]
```

---

## Polymorphism with Class Methods

Different classes can implement methods having the exact same signature:

```py
class India:
    def capital(self):
        return "New Delhi"

    def language(self):
        return "Hindi and English"

class France:
    def capital(self):
        return "Paris"

    def language(self):
        return "French"

def display_country_info(country):
    # Polymorphic function: does not care whether country is India or France
    print(f"Capital: {country.capital()} | Language: {country.language()}")

ind = India()
fra = France()

display_country_info(ind)  # Capital: New Delhi | Language: Hindi and English
display_country_info(fra)  # Capital: Paris | Language: French
```

---

## Duck Typing: The Python Way

Python relies on **Duck Typing**, a programming concept popularized by the phrase:

> *"If it walks like a duck and it quacks like a duck, then it's a duck."*

In Python, you do not check if an object explicitly belongs to a specific type or class hierarchy; you only check whether it implements the **behavior** (methods or attributes) that you need.

```py
class Duck:
    def quack(self):
        return "Quack, quack!"

class RoboticDuck:
    def quack(self):
        return "Beep boop, QUACK.wav playing!"

class PersonImpersonator:
    def quack(self):
        return "I'm pretending to be a duck: Quack!"

def make_it_quack(duck_like_object):
    # Only relies on the presence of .quack()
    print(duck_like_object.quack())

for entity in [Duck(), RoboticDuck(), PersonImpersonator()]:
    make_it_quack(entity)
```

---

## Polymorphism with Inheritance

Inheritance combined with method overriding allows derived classes to redefine common base actions:

```py
class AudioFile:
    def __init__(self, filename):
        self.filename = filename

    def play(self):
        raise NotImplementedError("Subclasses must implement play()")

class MP3File(AudioFile):
    def play(self):
        return f"Decompressing and playing MP3 stream for {self.filename}"

class WavFile(AudioFile):
    def play(self):
        return f"Playing uncompressed WAV audio for {self.filename}"

playlist: list[AudioFile] = [MP3File("song.mp3"), WavFile("sound_fx.wav")]

for track in playlist:
    print(track.play())
```

---

## Abstract Base Classes (ABCs) for Strict Contracts

When you want to enforce that all subclasses must implement specific methods, use Python's built-in `abc` module:

```py
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Must calculate and return shape area"""
        pass

    @abstractmethod
    def perimeter(self):
        """Must calculate and return shape perimeter"""
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side

# Trying to instantiate Shape directly raises TypeError:
# s = Shape() # TypeError: Can't instantiate abstract class Shape with abstract methods area, perimeter

sq = Square(4)
print(f"Square Area: {sq.area()}, Perimeter: {sq.perimeter()}")
```

---

## Real-World Design: Payment Processing Pipeline

Polymorphism makes payment gateways interchangeable without changing application checkout logic:

```py
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class PayPalGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Redirecting to PayPal for ${amount:.2f}... [Payment Verified]")
        return True

class StripeGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Charging Credit Card via Stripe for ${amount:.2f}... [Authorized]")
        return True

class CryptoGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Generating Bitcoin wallet invoice for ${amount:.2f}... [Confirmed]")
        return True

def checkout(cart_total: float, gateway: PaymentGateway):
    print(f"\n--- Initiating Checkout for ${cart_total:.2f} ---")
    success = gateway.process_payment(cart_total)
    if success:
        print("Order confirmed successfully!")

checkout(99.00, PayPalGateway())
checkout(149.50, StripeGateway())
checkout(300.00, CryptoGateway())
```

---

## Exercises

1. Create a notification system where classes `EmailNotification`, `SMSNotification`, and `PushNotification` all implement a `send(message)` method.
2. Write a function `notify_all(notifications_list, message)` that polymorphically triggers each sender.
3. Define an Abstract Base Class `DatabaseConnector` with abstract methods `connect()` and `disconnect()`, then implement `PostgreSQLConnector` and `MySQLConnector`.

---

[<< Previous: Python Inheritance](./08_python_inheritance.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Encapsulation >>](./10_python_encapsulation.md)
