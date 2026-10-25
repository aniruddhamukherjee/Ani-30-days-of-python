<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python Classes and Objects</h1>
</div>

[<< Previous: Python OOP](./01_python_oop.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python __init__ Method >>](./03_python_init_method.md)

---

- [📘 Day 21 - Python Classes and Objects](#-day-21---python-classes-and-objects)
  - [What is a Class?](#what-is-a-class)
  - [What is an Object?](#what-is-an-object)
  - [Creating a Class](#creating-a-class)
  - [Instantiating an Object](#instantiating-an-object)
  - [Class Attributes vs Instance Attributes](#class-attributes-vs-instance-attributes)
  - [Accessing and Modifying Attributes](#accessing-and-modifying-attributes)
  - [Deleting Attributes and Objects](#deleting-attributes-and-objects)
  - [Useful Built-in Inspection Functions](#useful-built-in-inspection-functions)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python Classes and Objects

## What is a Class?

A **class** is a user-defined blueprint or prototype from which objects are created. It defines a set of attributes (data) and methods (behavior) that the created objects will have.

Think of an architectural blueprint for a house:
- The blueprint itself is not a house you can live in.
- You can use the blueprint to construct multiple actual houses with distinct paint colors or furniture.

---

## What is an Object?

An **object** is an instance of a class. When a class is instantiated, memory is allocated, and the object can hold its own distinct state.

---

## Creating a Class

To define a class in Python, use the `class` keyword followed by the class name (by convention, using **PascalCase**) and a colon:

```py
class Dog:
    pass  # An empty class definition
```

---

## Instantiating an Object

An object is instantiated by calling the class name as if it were a function:

```py
# Creating objects (instances of Dog)
dog1 = Dog()
dog2 = Dog()

print(dog1)  # <__main__.Dog object at 0x000001FA2C...>
print(dog2)  # <__main__.Dog object at 0x000001FA2D...>
print(dog1 == dog2)  # False (different memory addresses)
```

---

## Class Attributes vs Instance Attributes

Understanding the difference between class attributes and instance attributes is essential:

- **Class Attributes**: Defined directly inside the class body; shared by **all instances** of the class.
- **Instance Attributes**: Assigned to an individual instance (typically inside `__init__`); unique to each object.

```py
class Student:
    # Class Attribute (shared by all students)
    school_name = "Python Academy"

    def __init__(self, name, grade):
        # Instance Attributes (unique to each student)
        self.name = name
        self.grade = grade

s1 = Student("Alice", 10)
s2 = Student("Bob", 12)

print(s1.name, "-", s1.school_name)  # Alice - Python Academy
print(s2.name, "-", s2.school_name)  # Bob - Python Academy

# Accessing class attribute via class name
print(Student.school_name)  # Python Academy
```

> [!NOTE]
> Modifying `Student.school_name` modifies it for all instances that haven't shadowed the attribute. Modifying `s1.school_name = "New School"` creates an instance attribute on `s1` only!

---

## Accessing and Modifying Attributes

Attributes are accessed and modified using **dot notation** (`.`):

```py
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.mileage = 0

car = Car("Toyota", "Corolla")

# Access attributes
print(f"Make: {car.make}, Model: {car.model}")

# Modify attribute
car.mileage = 15000
print(f"Mileage: {car.mileage} km")

# Add a new dynamic attribute on the fly
car.color = "Red"
print(f"Color: {car.color}")
```

---

## Deleting Attributes and Objects

You can delete an object attribute or the object itself using the `del` keyword:

```py
class Laptop:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

laptop = Laptop("Dell", 899)

# Deleting an attribute
del laptop.price
# print(laptop.price)  # Raises AttributeError: 'Laptop' object has no attribute 'price'

# Deleting the instance reference
del laptop
# print(laptop)        # Raises NameError: name 'laptop' is not defined
```

---

## Useful Built-in Inspection Functions

Python provides several built-in functions to inspect and manipulate classes and objects:

| Function | Description | Example |
| :--- | :--- | :--- |
| `isinstance(obj, class)` | Checks if `obj` is an instance of `class` | `isinstance(s1, Student)` -> `True` |
| `type(obj)` | Returns the class/type of the object | `type(s1)` -> `<class '__main__.Student'>` |
| `hasattr(obj, 'attr')` | Checks whether the object has the given attribute | `hasattr(s1, 'name')` -> `True` |
| `getattr(obj, 'attr', default)` | Gets the value of an attribute dynamically | `getattr(s1, 'name')` -> `'Alice'` |
| `setattr(obj, 'attr', val)` | Sets the value of an attribute dynamically | `setattr(s1, 'grade', 11)` |
| `delattr(obj, 'attr')` | Deletes an attribute dynamically | `delattr(s1, 'grade')` |

```py
class Book:
    def __init__(self, title):
        self.title = title

book = Book("Atomic Habits")
print(hasattr(book, "title"))            # True
print(getattr(book, "title"))            # Atomic Habits
print(getattr(book, "pages", "Unknown")) # Unknown (fallback default)
```

---

## Exercises

1. Create a class called `Point` that represents a point in 2D space $(x, y)$. Instantiate two points `p1 = Point(3, 4)` and `p2 = Point(7, 1)`.
2. Add a dynamic attribute `description` to `p1` and check if `p2` also has that attribute using `hasattr()`.
3. Create a class `Circle` with a class attribute `pi = 3.14159` and an instance attribute `radius`. Calculate the circumference.

---

[<< Previous: Python OOP](./01_python_oop.md) | [Day 21 Overview](./21_classes_and_objects.md) | [Next: Python __init__ Method >>](./03_python_init_method.md)
