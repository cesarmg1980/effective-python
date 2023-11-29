## Item 41: Consider Composing Functionality with Mix-in Classes

Note: **Avoid** Multiple inheritance.

What's a Mix-in Class?

* A Mix-in (or Mixin) class is a class that only defines a small set of additional methods that a child class will implement.
* Mix-in classes don't define their own attributes nor require a `__init__` constructor.
* Mix-ins can be composed together.

### Things to Remember

* Avoid using multiple inheritance with instance attributes and `__init__` if mixin classed can achieve the same result.
* Use pluggable behaviors at the instance level to provide per-class customization when mixin classes may require it.
* Mixins clan include instance methos or class methods.
* Compose Mixins to create complex functionality from simple behaviors.

## Item 42: Prefer Public Attributes over Private Ones

In Python there 2 types of visibility for a class's attribute:

1. `public`
2. `private`

Public attributes can be accesed by anyone using the dot operator (Obj.attribute)

Private fields are specified using a doule underscore (__attribute).

Example:

```
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10
```

Class methods also have access to private attributes

``` 
class MyOtherObject:
    def __init__(self):
        self.__private_field = 150

    @classmethod 
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field
```

A subclass cannot access the parent's private fields, in methods like `MyChildObject.get_private_field` it translates to `_MyChildObject.__private_field` but `_private_field` doesn't exist in `MyChildObject` it only exist in the `MyParentObject` and it gets translated to `_MyParentObject.__private_field` which is different from `_MyChildObject.__private_field`

### Things to remeber:

* Private attributes aren't rigorously enforced by the Python compiler.
* Plan from the beginning to allow subclasses to do more with your internal APIs and attributes instead of choosing to lock them out.
* Use documentation of protected fields to guide subclasses instead of trying to force access control with private attributes.
* Only consider using private attributes to avoid naming conflicts with subclasses that are out of control.

## Item 43: Inherit from `collection.abc` for Custom Container Types

```
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
       counts = {}
       for item in self:
           counts[item] = counts.get(item, 0) + 1
        return counts 
```

When subclassing from `list` you get all the list's standars functionality and also you can preserve the same semantics.

But in the following example:

```
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f"Index {index} is out of range")
```

if you try to do call `len` on the object you will get an exeption because `len` wan't implemented only `__getitem__`
If you want for an object to be able to do `len` you need to implement `__len__`

You inherit from `collection.abc` to get a more appropriate `container` behavior, but you will need to implement some methods yourself *see example item.43.py*

### Things to Remember

* Inherit from Python's container types 'list' and 'dict' for simple use cases.
* Beware of large number of methods that you need to implement custom-container.
* Have your custom containers inherit from `collections.abc` to be sure that you're implementing all the methods required and to get the desired behavior.
