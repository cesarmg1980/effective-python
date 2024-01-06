import json


class Serializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"


print()
print("### Example 1 ###")
point = Point2D(5, 3)
print('Object:  ', point)
print('Serialized:', point.serialize())


class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class BetterPoint2D(Point2D, Deserializable):
    pass


print()
print("### Example 2 ###")
before = BetterPoint2D(5, 3)
print("Before:", before)
data = before.serialize()
print("Serialized:", data)
after = BetterPoint2D.deserialize(data)
print("After:", after)


"""
In this example we're trying to make the deserialization process
agnostic, meaning that we don't need to know in advance what's the class to be
deserialized
"""
class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps(
            {
                "class": self.__class__.__name__,
                "args": self.args,
            }
        )

    def __repr__(self):
        name = self.__class__.__name__
        args_str = '. '.join(str(x) for x in self.args)
        return f"{name}({args_str})"


"""
This Var will hold a register of the classes to be deserialized
"""
registry = {}


"""
This method will add the target class to the registry
"""
def register_class(target_class):
    registry[target_class.__name__] = target_class


"""
This method actually deserializes the input data into the class that's been
registered
"""
def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y


register_class(EvenBetterPoint2D)

print()
print("### Example 3 ###")
before = EvenBetterPoint2D(5, 3)
print("Before: ", before)
data = before.serialize()
print("Serialized: ", data)
after = deserialize(data)
print("After: ", after)


"""
The problem with the above approach is that you can forget to call
'register_class', see below example
"""
class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z


point = Point3D(5, 9 , -4)
data = point.serialize()
try:
    deserialize(data)
except KeyError as ex:
    print(f"Error: {ex.args[0]}")


"""
Using Metaclass to register the class immediately after the class's body
"""
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z


print()
print("### Example 4 ###")
before = Vector3D(10, -7, 3)
print("Before: ", before)
data = before.serialize()
print("Serialized: ", data)
print("After: ", deserialize(data))



"""
An even better approach is to use the `__init_subclass__`, much less visual
noise, and more simple of reading
"""
class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)


class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude


print()
print("### Example 5 ###")
before = Vector1D(6)
print("Before: ", before)
data = before.serialize()
print("Serialized: ", data)
print("After: ", deserialize(data))
