class LazyRecord:
    def __init__(self):
        self.attribute_already_existing = 5

    def __getattr__(self, name):
        value = f"Value for {name}"
        setattr(self, name, value)
        return value

"""Here I instantiate LazyRecord, show the object's status before adding a new
attribute, add a new attribute to the object and finally show again the
object's status"""
print("## Example 1 ##")
data = LazyRecord()
print("Object's Status before: ", data.__dict__)
print("Adding new attribute to Object", data.new_attrib)
print("Object Status after: ", data.__dict__)


class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f"* called __getattr__({name!r}), populating instance dictionary")
        result = super().__getattr__(name)
        print(f"* Returning {result!r}")
        return result


"""The 'attribute_already_existing' already exists so __getattr__ is never
called for it, then 'new_attrib' doesn't exists so __getattr__ gets called for
it, but the last time is not called because the attribute was already created"""
print()
print("## Example 2 ##")
data = LoggingLazyRecord()
print("Attribute already existing: ", data.attribute_already_existing)
print("First new_attrib: ", data.new_attrib)
print("Second new_attrib: ", data.new_attrib)


class ValidatingRecord:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print(f"* Called __getattribute__({name!r})")
        try:
            value = super().__getattribute__(name)
            print(f"* Found {name!r}, returning {value!r}")
            return value
        except AttributeError:
            value = f"Value for {name}"
            print(f"* Setting {name!r} to {value!r}")
            setattr(self, name, value)
            return value


print()
print("## Example 3 ##")
data = ValidatingRecord()
print('exists: ', data.exists)
print('first foo: ', data.foo)
print('second foo: ', data.foo)


"""Python code that implements generic functionality often relies on `hasattr`
builtin function to determine when a property exists, and the `getattr` builtin
function to retrieve the property's value. These functions also look into the
instance's __dict__ dictionary before calling `__getattr`"""
print()
print("## Example 4 ##")
data = LoggingLazyRecord()  # Implementes __getattr__
print('Before: ', data.__dict__)
print('Has first foo: ', hasattr(data, 'foo'))
print('After: ', data.__dict__)
print('Has second foo: ', hasattr(data, 'foo'))


print()
print("## Example 5 ##")
data = ValidatingRecord()  # Implements __getattribute__
print('has first foo: ', hasattr(data, 'foo'))
print('has second foo: ', hasattr(data, 'foo'))


class SavingRecord:
    def __setattr__(self, name, value):
        # Save some data for the record
        ...
        super().__setattr__(name, value)


class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f"* Called __setattr__({name!r}, {value!r})")
        super().__setattr__(name, value)


print()
print("## Example 6 ##")
data = LoggingSavingRecord()
print('Before: ', data.__dict__)
data.foo = 5
print('After: ', data.__dict__)
data.foo = 7
print('Finally: ', data.__dict__)


class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print(f"* Called __getattribute__({name!r})")
        data_dict = super().__getattribute__('_data')
        return data_dict[name]


print()
print("## Example 7 ##")
datat = DictionaryRecord({"foo": 3})
print('foo: ', data.foo)
