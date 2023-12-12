## Chapter 6 - Metaclasses and Attributes

### Item 44: Use plain attributes instead of `setter` and `getter` methods

Don't implement explicit `setter` and `getter` methods, instead start your implementations with simple public attributes.

```
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3

# It's easier later to do:

r1.ohms += 5e3
```

If you find out later that you need to change an attribute's behavior when it's set you can use the `@property` decorator and its `setter` attribute *see example*

When you specify a setter on a property it allows you to perform validations before setting the value *see example*

Don't set other attributes other than the one that the `setter` is supposed to set

```
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current # DON'T DO THIS
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms
```

#### Things to remember

* Define new classes using simple public attributes
* Use @property to define special beaviors
* Avoid side effects when using @property
* Ensure @property methods are fast, for slow/complex work use regular methods

### Item 45: Consider `@property` instead of refactoing attributes.

*see item-45.py example*

#### Things to remember

* User `@property` to give existing instance attributes new functionalities.
* Use `@property` to make incremental progress towards better data models.
* Is you're using `@property` too much start considering refactoring.

### Item 46: Use Descriptors for Reusable `@property` Methods

The "Descriptor" protocol defines how attribute access is going to be interpreted by the language.
A Descriptor Class provides `__set__` and `__get__` methods.

*See Example "item-46.py"*

What Python does when these "descriptor" attributes are accesed:

```
exam = Exam()  # here we're creating an instance of Exam class
exam.writing_grade = 40  # here we're assigning 40 to the 'writing_grade' attribute'

#  The above line is intepreted as:
Exam.__dict__['writing_grade'].__set__(exam, 40)

# When i retrieve the property
exam.writing_grade

# This gets translated into:
Exam.__dict__['writing_grade'].__get__(exam, Exam)
```

### Things to Remember

* Reuse the behavior and validation of `@property` methods by defining your own descriptor classes.
* Use `WeakKeyDictionary` to ensure your descriptor classes don't cause memory leaks.
