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
