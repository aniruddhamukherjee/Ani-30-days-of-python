<div align="center">
  <h1> 30 Days Of Python: Day 21 - Python Inner Classes</h1>
</div>

[<< Previous: Python Encapsulation](./10_python_encapsulation.md) | [Day 21 Overview](./21_classes_and_objects.md)

---

- [📘 Day 21 - Python Inner Classes](#-day-21---python-inner-classes)
  - [What is an Inner Class?](#what-is-an-inner-class)
  - [Why Use Inner Classes?](#why-use-inner-classes)
  - [Basic Syntax and Instantiation](#basic-syntax-and-instantiation)
    - [Method 1: Instantiating Inside Outer Class](#method-1-instantiating-inside-outer-class)
    - [Method 2: Instantiating Directly from Outside](#method-2-instantiating-directly-from-outside)
  - [Complex Example: Multiple Inner Classes](#complex-example-multiple-inner-classes)
  - [Accessing Outer Class Members from Inner Class](#accessing-outer-class-members-from-inner-class)
  - [Real-World Usage: Django & Pydantic](#real-world-usage-django--pydantic)
  - [When to Use vs When to Avoid Inner Classes](#when-to-use-vs-when-to-avoid-inner-classes)
  - [Exercises](#exercises)

---

# 📘 Day 21 - Python Inner Classes

## What is an Inner Class?

An **inner class** (or **nested class**) is a class defined completely inside another enclosing class.

```py
class Outer:
    class Inner:
        pass
```

The inner class is scoped within the namespace of the outer class, meaning it is accessible via `Outer.Inner`.

---

## Why Use Inner Classes?

1. **Logical Grouping**: If a helper class is only useful in the context of one parent class, nesting it prevents polluting the module-level namespace.
2. **Encapsulation**: Keeps tightly coupled components together.
3. **Readability and Organization**: Clearly communicates to readers that the inner class belongs conceptually to the outer class.

---

## Basic Syntax and Instantiation

### Method 1: Instantiating Inside Outer Class

This is the most common pattern. The outer class creates and manages instances of the inner class within its own `__init__`:

```py
class Student:
    def __init__(self, name, roll_no, brand, cpu, ram_gb):
        self.name = name
        self.roll_no = roll_no
        # Instantiating the inner Laptop class inside Student
        self.laptop = self.Laptop(brand, cpu, ram_gb)

    def show(self):
        print(f"Student: {self.name} (Roll: {self.roll_no})")
        self.laptop.show()

    # Inner Class definition
    class Laptop:
        def __init__(self, brand, cpu, ram_gb):
            self.brand = brand
            self.cpu = cpu
            self.ram_gb = ram_gb

        def show(self):
            print(f"  Laptop Specs: {self.brand}, {self.cpu}, {self.ram_gb}GB RAM")

s1 = Student("John", 101, "Apple", "M2", 16)
s1.show()
# Student: John (Roll: 101)
#   Laptop Specs: Apple, M2, 16GB RAM
```

---

### Method 2: Instantiating Directly from Outside

You can also create an instance of the inner class directly from outside by accessing it through the outer class namespace:

```py
# Instantiating through the Outer class namespace:
independent_laptop = Student.Laptop("Dell", "Intel i7", 32)
independent_laptop.show()
#   Laptop Specs: Dell, Intel i7, 32GB RAM
```

---

## Complex Example: Multiple Inner Classes

A class can contain multiple inner classes to model closely coupled subsystems:

```py
class Car:
    def __init__(self, make, model, hp, gear_count):
        self.make = make
        self.model = model
        self.engine = self.Engine(hp)
        self.transmission = self.Transmission(gear_count)

    def start(self):
        print(f"Starting {self.make} {self.model}...")
        self.engine.ignite()
        self.transmission.engage(1)

    class Engine:
        def __init__(self, horsepower):
            self.horsepower = horsepower

        def ignite(self):
            print(f"  Vroom! {self.horsepower} HP engine ignited.")

    class Transmission:
        def __init__(self, gears):
            self.gears = gears
            self.current_gear = 0

        def engage(self, gear):
            if 0 <= gear <= self.gears:
                self.current_gear = gear
                print(f"  Transmission engaged to gear {self.current_gear}.")

car = Car("Ford", "Mustang", 450, 6)
car.start()
```

---

## Accessing Outer Class Members from Inner Class

Unlike some languages (like Java), an inner class instance in Python does **not** automatically have an implicit reference to its enclosing outer instance. If the inner class needs to access outer attributes, pass the outer instance (`self`) explicitly:

```py
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []

    def add_item(self, name, price):
        # Passing self (the order) to the LineItem
        item = self.LineItem(self, name, price)
        self.items.append(item)
        return item

    class LineItem:
        def __init__(self, order, name, price):
            self.order = order  # Reference to outer Order instance
            self.name = name
            self.price = price

        def get_receipt_line(self):
            return f"[{self.order.order_id}] {self.name}: ${self.price:.2f}"

order = Order("ORD-5541")
item1 = order.add_item("Mechanical Keyboard", 120.00)
item2 = order.add_item("Wireless Mouse", 50.00)

print(item1.get_receipt_line())  # [ORD-5541] Mechanical Keyboard: $120.00
print(item2.get_receipt_line())  # [ORD-5541] Wireless Mouse: $50.00
```

---

## Real-World Usage: Django & Pydantic

Inner classes are popular in major Python frameworks for configuration and metadata:

### 1. Django Models (`class Meta`)
```py
# Conceptual Django model example:
class Article:
    title = "My Blog Post"

    class Meta:
        ordering = ['-title']
        verbose_name = "Blog Article"
```

### 2. Pydantic / SQLAlchemy (`class Config`)
```py
# Conceptual Pydantic model example:
class UserModel:
    name: str

    class Config:
        frozen = True
        str_strip_whitespace = True
```

---

## When to Use vs When to Avoid Inner Classes

| Recommended to Use | Better to Avoid |
| :--- | :--- |
| Helper classes strictly tied to one parent class | Classes that will be reused by multiple entities across the project |
| Configuration metadata (e.g. `Meta` or `Config`) | Deep nesting (e.g. class inside class inside class) which hurts readability |
| Modeling composite components with tight encapsulation | When a simple top-level class in the same module is clearer |

---

## Exercises

1. Create a `Computer` class with an inner class `OperatingSystem` that tracks OS name and version.
2. Create a `LinkedList` class with an inner `Node` class containing `data` and `next`.
3. Add a method in `LinkedList` to append a node using the inner `Node` class.

---

[<< Previous: Python Encapsulation](./10_python_encapsulation.md) | [Day 21 Overview](./21_classes_and_objects.md)
