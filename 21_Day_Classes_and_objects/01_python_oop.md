<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python OOP</h1>
</div>

[<< Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Classes & Objects >>](./02_python_classes_objects.md)

---

- [📘 Day 21 - Python OOP](#-day-21---python-oop)
  - [What is Object-Oriented Programming (OOP)?](#what-is-object-oriented-programming-oop)
  - [Procedural vs Object-Oriented Programming](#procedural-vs-object-oriented-programming)
  - [The Four Core Pillars of OOP](#the-four-core-pillars-of-oop)
    - [1. Encapsulation](#1-encapsulation)
    - [2. Abstraction](#2-abstraction)
    - [3. Inheritance](#3-inheritance)
    - [4. Polymorphism](#4-polymorphism)
  - [Why Use OOP in Python?](#why-use-oop-in-python)
  - [A High-Level Preview](#a-high-level-preview)
  - [Key Takeaways](#key-takeaways)

---

# 📘 Day 21 - Python OOP

## What is Object-Oriented Programming (OOP)?

**Object-Oriented Programming (OOP)** is a programming paradigm based on the concept of **objects**. Objects contain data in the form of **attributes** (often known as variables or fields) and behavior in the form of **methods** (functions associated with the object).

In Python, **everything is an object**. Numbers, strings, lists, dictionaries, functions, and even modules are objects under the hood.

```py
# Checking the type of built-in entities
print(type(42))            # <class 'int'>
print(type("Python"))      # <class 'str'>
print(type([1, 2, 3]))     # <class 'list'>
print(type({'a': 1}))      # <class 'dict'>
```

---

## Procedural vs Object-Oriented Programming

| Feature | Procedural Programming | Object-Oriented Programming (OOP) |
| :--- | :--- | :--- |
| **Focus** | Step-by-step procedures and functions | Data and behavior encapsulated in objects |
| **Structure** | Code is organized into functions | Code is organized into classes and objects |
| **Data Access** | Data is often global or passed between functions | Data is tightly bound within objects |
| **Reusability** | Limited code reuse (copy-paste or nested functions) | High code reuse via inheritance and composition |
| **Maintenance** | Harder to maintain as codebase grows | Easier to maintain, scale, and refactor |

### Procedural Approach Example:
```py
# Data and logic are separated
car_brand = "Tesla"
car_speed = 0

def accelerate(speed, increment):
    return speed + increment

car_speed = accelerate(car_speed, 20)
print(f"{car_brand} speed: {car_speed} km/h")
```

### Object-Oriented Approach Example:
```py
# Data and behavior are bundled together
class Car:
    def __init__(self, brand):
        self.brand = brand
        self.speed = 0

    def accelerate(self, increment):
        self.speed += increment

my_car = Car("Tesla")
my_car.accelerate(20)
print(f"{my_car.brand} speed: {my_car.speed} km/h")
```

---

## The Four Core Pillars of OOP

Object-Oriented Programming is built on four primary principles:

### 1. Encapsulation
Encapsulation bundles data (attributes) and the methods that operate on that data into a single unit (a class), restricting direct external access to prevent unintended interference.

```py
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance
```

### 2. Abstraction
Abstraction hides complex implementation details and exposes only the essential features to the user. For example, when you drive a car, you press the gas pedal without needing to know how the fuel injection system works.

### 3. Inheritance
Inheritance allows a new class (child or subclass) to inherit attributes and methods from an existing class (parent or superclass), promoting code reuse.

```py
class Animal:
    def eat(self):
        return "Eating..."

class Dog(Animal):
    def bark(self):
        return "Woof!"
```

### 4. Polymorphism
Polymorphism (meaning "many shapes") allows different classes to implement methods with the same name, enabling a single interface to control different types of objects.

```py
class Bird:
    def speak(self):
        return "Chirp chirp"

class Cat:
    def speak(self):
        return "Meow"

for animal in [Bird(), Cat()]:
    print(animal.speak())
```

---

## Why Use OOP in Python?

1. **Modularity**: Classes keep distinct concepts separated and well-organized.
2. **Reusability**: Write once, instantiate many times, or extend through inheritance.
3. **Maintainability**: Bugs can often be isolated to specific classes without affecting the rest of the application.
4. **Real-world Modeling**: Objects represent real-world entities (Users, Products, Orders, HTTP Requests) naturally.

---

## A High-Level Preview

The topics covered in Day 21 include:
1. **Python OOP**: Core philosophy and principles (Current Module).
2. **[Python Classes/Objects](./02_python_classes_objects.md)**: Defining blueprints and instantiating them.
3. **[Python `__init__` Method](./03_python_init_method.md)**: Object initialization and constructors.
4. **[Python `self` Parameter](./04_python_self_parameter.md)**: Understanding instance reference.
5. **[Python Class Properties](./05_python_class_properties.md)**: Managing attributes with `@property`, getters, and setters.
6. **[Python Class Methods](./06_python_class_methods.md)**: Instance vs `@classmethod` vs `@staticmethod`.
7. **[Python Magic Methods](./07_python_magic_methods.md)**: Dunder methods and operator overloading.
8. **[Python Inheritance](./08_python_inheritance.md)**: Subclassing, `super()`, and MRO.
9. **[Python Polymorphism](./09_python_polymorphism.md)**: Duck typing and abstract interfaces.
10. **[Python Encapsulation](./10_python_encapsulation.md)**: Public, protected, private attributes and data hiding.
11. **[Python Inner Classes](./11_python_inner_classes.md)**: Nesting classes for modular design.

---

## Key Takeaways

- OOP is a paradigm centering around **Classes** (blueprints) and **Objects** (instances).
- Python supports multiple paradigms: procedural, object-oriented, and functional.
- The 4 pillars are **Encapsulation**, **Abstraction**, **Inheritance**, and **Polymorphism**.

[<< Day 21 Overview](./21_classes_and_objects.md) | [Next: Python Classes & Objects >>](./02_python_classes_objects.md)
