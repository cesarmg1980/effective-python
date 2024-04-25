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


print("### Item 50: Annotate Class Attributes with '__set_name__'")
print()
cust = Customer()
print(f"Before: {cust.first_name!r} {cust.__dict__}")
cust.first_name = 'Euclid'
print(f"After: {cust.first_name!r} {cust.__dict__}")


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


print()
print("Example with Metaclass")
try:
    cust = BetterCustomer()
    print(f"Before: {cust.first_name!r} {cust.__dict__}")
    cust.fist_name = 'Euler'
    print(f"After: {cust.first_name!r} {cust.__dict__}")
except TypeError as ex:
    print(f"Error: {ex.args[0]} << == Not in the book")


class Field2:
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

class FixedCustomer:
    first_name = Field2()
    last_name = Field2()
    prefix = Field2()
    suffix = Field2()

print()
print("Example with '__set_name__'")
cust = FixedCustomer()
print(f"Before: {cust.first_name!r} {cust.__dict__}")
cust.first_name = "Marsenne"
print(f"After: {cust.first_name!r} {cust.__dict__}")
