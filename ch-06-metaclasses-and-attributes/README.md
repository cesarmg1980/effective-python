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

#### Things to Remember

* Reuse the behavior and validation of `@property` methods by defining your own descriptor classes.
* Use `WeakKeyDictionary` to ensure your descriptor classes don't cause memory leaks.

### Item 47: Use `__getattr__`, `__getattribute__` and `__setattr__` for Lazy Attributes 

`__getattr` is a method that is called everytime an object's attribute can't be found in the object's dictionary.

*See Example item-47.py*

Python has another object hook called `__getattribute__`, this special method is called **every** time an attribute is called on an object, even if it already exists

*See Example item-47.py*

classes that implement `__getattr__` gets this method called only once while classes that implements `__getattribute__`  have this method called each time `hasattr` or `getattr` is used with an instance.

*See Example #5 in item-47.py*

`__setattr__` another object hook that allows you to intercept attribute assignment.
the `__setattr__` is always called every time an attribute is assigned on an instance.

`__getattr__` and `__setattr__` they're called on **every** attribute access for an object.

```
class BrokenDictionaryRecord:
    def __init__(self data):
        self.data = {}

    def __getattribute__(self, name):
        print(f"* Called __getattribute__({name!r})")
        return self._data[name]

# This requires accessing self._data from within the __getattribute__ 
# which will result in recursion until reaches the stack limit.

data = BrokenDictionaryRecord({"foo": 3})
data.foo

>>>
* Called __getattribute__('foo')
* Called __getattribute__('foo')
* Called __getattribute__('foo')
* Called __getattribute__('foo')
...
Traceback ...
RecursionError: maximum recursion depth...
```

*See Example #7 for a working solution*

Note: `__setattr__` methods also need to call `super().__setattr__` 

### Things to remember

* Use `__getattr__` and `__setattr__` to lazily load and save attributes for an object.
* `__getattr__` **only** gets called when accessing a missing attribute, `__getattribute__` gets called **every** time an attribute is accessed.
* Avoid infinite recursion in `__getattribute__` and `__setattr__` by using methods from `super()` i.e: `super().__getattribute__`


## Item 48: validate sublasses with __init__subclass__

A `Metaclass` is defined by inheriting from `type`
You can add functionality to the `Meta.__new__` in order to validate the parameters of a class before it's defined.
Python 3.6 introduced `__init__subclass__()` to avoid the use of `Metaclass`
You can only specify a single `metaclass` per class definition.
Example 7, 8 and 8 shows that we can achieve multiple validations with `metaclass` but it's complicated and is you want to reuse this for another set of class hierarchies then you would need to duplicate all the code on the other set of classes.
You can even use `__init__subclass__` in complex cases like diamond hierarchies.

### Things to Remember

* The `__new__` method of metaclasses is run after the entire class statement's entire body has been processed.
* Metaclasses can be used to inspect/modify a class after it's defined but **before** it's created, but they're often more heavyweight than what you need.
* Use `__init__subclass__` to ensure that subclasses are well formed at the time they're defined, before objects of their tipe are constructed.
* Be sure to call `super().__init_subclass__` from within your class's `__init_subclass__` definition to enable validation in multiple layers of classes and multiple inheritance.


## Item 49: Register class existence with `__init_subclass__`

*See Examples*

### Things to Remember

* Class registration is a useful pattern for building modular Python programs
* Metaclasses let you run registration code automatically each time a base class is subclassed in a program.
* Using metaclass for class registration helps you avoid errors like forgetting registering a class.
* Prefer `__init_subclass__` over `metaclass` because it's clearer and easy to understand.


## Item 50: Annotate Class Attributes with `__set_name__`

Another useful capability of metaclasses is to modify or annotate properties after a class is defined but before the class is instantiated.

```
class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer:
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')
```

Why do we need to also specify the name (`first_name = Field('first_name')`)?

This is the actual order of operations:

1. `Field('first_name')` is called
2. The output of the above is assigned to `Customer.first_name`

There's no way for `Field` to know beforehand what attribute to assign itself to.

This is where it enters metaclasses. Metaclasses lets you hook the class statement direcly and do something as soon as the class body is finished.

``` 
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


class DatabaseRow(metaclass=Meta):
    pass


class NewField:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class BetterCustomer(DatabaseRow):
    first_name = NewField()
    last_name = NewField()
    prefix = NewField()
    suffix = NewField()
```

But this causes the following error:

```
Error: getattr(): attribute name must be string
```

Here is where `__set_name__` enters. It is called on the descriptor instance.
It receives as parameters the owning class that contains the decriptor and the attribute to which the descriptor is attached

See example below:

```

class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        # Called on class creation for each descriptor
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)
```

### Things to Remember

- Metaclass lets you modify classes's attributes bebore the class is fully defined
- Descriptors and Metaclasses make a powerful combination for declarative behavior and runtime introspection
- Define `__set_name__` on your descriptor classes to allow them to take into account their surrounding class and its property names
- Avoid memory leaks and the `weakref` built-in module by having descriptors store data they manipulate directly within a class's instance dictionary


## Item 51: Prefer Class Decorators over Metaclasses for composable class extension

This Code below
```
def trace_func(func):
    if hasattr(func, 'tracing'):  # Only decorate once
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")

    wrapper.tracing = True
    return wrapper


class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)
```

Produces the following output:
```
__init__(({'hi': 1}, [('hi', 1)]), {}) -> None
__setitem__(({'hi': 1, 'there': 2}, 'there', 2), {}) -> None
__getitem__(({'hi': 1, 'there': 2}, 'hi'), {}) -> 1
__getitem__(({'hi': 1, 'there': 2}, 'does not exist'), {}) -> KeyError('does not exist')
```

The `@trace_func` decorator inspects the decorated function and shows the arguments received and the return value

But the problem with the above approach is that i'll need to redefine each method

Like this:
```
@trace_func
def __setitem__(self, *args, **kwargs):
    return super().__setitem__(*args, **kwargs)
```

This means that if afterwards, a new method is added to the `dict` superclass, it won't be decorated unless i redefine it in my `TraceDict` class

One way to solve this is to create a Metaclass that automatically decorates all methods.
```
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)
        return klass

class TraceDict(dict, metaclass=TraceMeta):
    pass
```

If you try to use a Metaclass on a class that has a superclass that already has a Metaclass (see example below):
```
class OtherMeta(type):
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    pass

class TraceDict(SimpleDict, metaclass=TraceMeta):
    pass
```

You would get the following error:
```
Error: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
```
This causes an error because TraceMeta does not inherit from OtherMeta

One way to fix this is to make OtherMeta inherit from TraceMeta
```
class OtherMeta(TraceMeta):
    pass
```

A better approach to all of this is to use `class` decorators, class decorators are just like `function` decorators, they're used with the `@` simbol, the function is expected to modify or re-create the class accordingly and return it.
```
def my_class_decorator(klass):
    klass.extra_param = 'hello'
    return klass


@my_class_decorator
class MyClass:
    pass
```

Given the above i can implement a class decorator to apply `trace_func` to all methods of a class
```
def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass


@trace
class TraceDict(dict):
    pass
```

Class decorators also work with classes that already have other Metaclasses 
```
class OtherMeta(type):
    pass


@trace
class TraceDict(dict, metaclass=OtherMeta):
    pass
```

When you want composable ways to extend your classes: Use Class Decorators

#### Thing to Remember
- Class Decorators are simple functions that receive a class as a parameter and returns either a new class or a modified version of the class
- Class Decorators are useful when you want to modify all methods or attributes of a class with minimal boilerplate
- Metaclass can't be composed together easyly, while many class decorators can be used to extend the same class without problems.
