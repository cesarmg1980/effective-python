class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


print()
print("### Example 1 ###")
foo = MyObject()
print(f"Public Attribute: foo.public_field == 5 is {foo.public_field == 5}")
print(f"Private Attribute accessed through a method: foo.get_private_field() == 10 is {foo.get_private_field() == 10}")
print("Private Attribute cannot be accesed by Obj.__private_field: ", end='')
try:
    foo.__private_field
except AttributeError as ex:
    print(f"Error: {ex.args[0]}")


class MyOtherObject:
    def __init__(self):
        self.__private_field = 150

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field
print()
print("### Example 2 ###")
bar = MyOtherObject()
print(f"MyOtherObject.get_private_field_of_instance(bar) == 150 is {MyOtherObject.get_private_field_of_instance(bar) == 150}")


class MyParentObject:
    def __init__(self):
        self.__private_field = "foobar"

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

print()
print("### Example 3 ###")
baz = MyChildObject()
print("Private Attribute from parent class cannot be accesed by MyChildObject.get_private_field: ", end='')
try:
    baz.get_private_field()
except AttributeError as ex:
    print(f"Error: {ex.args[0]}")
