"""
Example with a function decorator
"""
from functools import wraps


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


print("### Example 1 - with trace decorator ###")
trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected

"""
Example with Metaclass
"""
import types

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType
)

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

print()
print("### Example 2 - with TraceMeta ###")
trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected

"""
Here i try to use a metaclass on a class that has a super class that already has another metaclass
"""
try:
    class OtherMeta(type):
        pass

    class SimpleDict(dict, metaclass=OtherMeta):
        pass

    class TraceDict(SimpleDict, metaclass=TraceMeta):
        pass
except Exception as e:
    print()
    print("### Example 3 - Using a Metaclass that has a superclass that already has a Metaclass ###")
    print("""
    class OtherMeta(type):
        pass

    class SimpleDict(dict, metaclass=OtherMeta):
        pass

    class TraceDict(SimpleDict, metaclass=TraceMeta):
        pass
          """)
    print(f"Error: {e.args[0]}")


class OtherMeta(TraceMeta):
    pass


class SimpleDict(dict, metaclass=OtherMeta):
    pass


class TraceDict(SimpleDict, metaclass=TraceMeta):
    pass

print()
print("### Example 4 - Making OtherMeta inheriting from TraceMeta")
print("""
class OtherMeta(TraceMeta):
    pass
      """)
trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does_not_exist']
except KeyError:
    pass  # Expected


def my_class_decorator(klass):
    klass.extra_param = 'hello'
    return klass


@my_class_decorator
class MyClass:
    pass


print()
print("### Example 5 - Class decorators")
print("""
def my_class_decorator(klass):
    klass.extra_param = 'hello'
    return klass


@my_class_decorator
class MyClass:
    pass
      """)
print(f">>> {MyClass}")
print(f">>> {MyClass.extra_param}")


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


print()
print("### Example 6 - Class Decorator")
print("""
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
      """)
trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected


class OtherMeta(type):
    pass


@trace
class TraceDict(dict, metaclass=OtherMeta):
    pass

print()
print("### Example 7 - Class Decorators also works with Classes that already have other Metaclasses")
print("""
class OtherMeta(type):
    pass


@trace
class TraceDict(dict, metaclass=OtherMeta):
    pass
      """)
trace_dict = TraceDict([('hi', 1)])
trace_dict['there'] = 2
trace_dict['hi']
try:
    trace_dict['does not exist']
except KeyError:
    pass  # Expected
