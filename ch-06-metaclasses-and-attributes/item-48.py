"""
This example shows how Metaclasses have access to all the Class's attributes
even at the time that the module is loaded
"""

print("### Example 1 ###")
class Meta(type):
    def __new__(meta, name ,bases, class_dict):
        print(f"* Running {meta}.__new__ for {name}")
        print("Bases: ", bases)
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass


class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass


"""In this example i'm adding validations for a Polygon class"""
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate subclasses of the Polygon class
        if bases:
            if class_dict['sides'] < 3:
                raise ValueError("A Polygon needs 3+ sides")
        return type.__new__(meta, name ,bases, class_dict)


class Polygon(metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


class Rectangle(Polygon):
    sides = 4


class Nonagon(Polygon):
    sides = 9


print()
print("### Example 2 ###")
print(f"Triangle.interior_angles() == 180: {Triangle.interior_angles() == 180}")
print(f"Rectangle.interior_angles() == 360: {Rectangle.interior_angles() == 360}")
print(f"Nonagon.interior_angles() == 1260: {Nonagon.interior_angles() == 1260}")


"""But here i try to define a class that has just 2 sides and i get an error
that is thrown by the ValidatePolygon metaclass"""
print()
print("### Example 3 ###")
try:
    class Line(Polygon):
        print("Before sides")
        sides = 2
        print("After sides")
except ValueError as ex:
    print(f"Error: {ex.args[0]}")


"""
This example uses __init_subclass__ instead of Metaclass
"""
class BetterPolygon:
    sides = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError("Polygon needs 3+ sides")

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Hexagon(BetterPolygon):
    sides = 6


print()
print("### Example 4 ###")
print(f"Hexagon.interior_angles() == 720: {Hexagon.interior_angles() == 720}")


print()
print("### Example 5 ###")
try:
    class Point(BetterPolygon):
        sides = 1
except ValueError as ex:
    print(f"Error: {ex.args[0]}")


"""
Using Metaclasses for multiple validations creates some complications
"""
class ValidateFilled(type):
    def __new__(meta, name, bases, class_dict):
        #  Only validate subclasses of the Filled class
        if bases:
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Fill color must be supported')
        return type.__new__(meta, name, bases, class_dict)


class Filled(metaclass=ValidateFilled):
    color = None  # Must be specified by subclasses


print()
print("### Example 6 ###")
try:
    class RedPentagon(Filled, Polygon):
        color = 'red'
except TypeError as ex:
    print(f"Error: {ex.args[0]}")
    sides = 5


class ValidatePolygon2(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['sides'] < 3:
                raise ValueError("Polygons need 3+ sides")
        return type.__new__(meta, name, bases, class_dict)


class Polygon2(metaclass=ValidatePolygon2):
    is_root = True
    sides = None  # Must be specified by subclasses


class ValidateFilledPolygon(ValidatePolygon2):
    def __new__(meta, name, bases, class_dict):
        #  Only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError("Fill color must be supported")
        return super().__new__(meta, name, bases, class_dict)


class FilledPolygon(Polygon2, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None  # Must be specified by subclasses

"""
This requires every `FilledPolygon` instance to be a `Polygon` instance
"""
class GeenPentagon(FilledPolygon):
    color = 'green'
    sides = 5


print()
print("### Example 7 ###")
greenie = GeenPentagon()
print(f"assert isinstance(greenie, Polygon2): {isinstance(greenie, Polygon2)}")

"""
Validation works for colors
"""
print()
print("### Example 8 ###")
try:
    class OrangePentagon(FilledPolygon):
        color = 'orange'
        sides = 5
except ValueError as ex:
    print(f"Error: {ex.args[0]}")


"""
Validation also works for number of sides
"""
print()
print("### Example 9 ### ")
try:
    class RedLine(FilledPolygon):
        color = 'red'
        sides = 2
except ValueError as ex:
    print(f"Error: {ex.args[0]}")


class Fileld:
    color = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError("Filled need a valid color")

"""
I can inherit from both classes to define a new class, both classes call
super().__init_subclass__(), making the validation run when the subclass is
created
"""
class RedTriangle(Filled, BetterPolygon):
    color = 'red'
    sides = 3

print()
print("### Example 10 ###")
ruddy = RedTriangle()
print(f"assert isinstance(ruddy, Filled): {isinstance(ruddy, Filled)}")
print(f"assert isinstance(ruddy, BetterPolygon): {isinstance(ruddy, BetterPolygon)}")


"""
If i specify an incorrect number of sides or colors i get an error
"""
print()
print("### Example 11 ###")
try:
    class BlueLine(Filled, BetterPolygon):
        color = 'blue'
        sides = 2
except ValueError as ex:
    print(f"Error: {ex.args[0]}")
print("There's an error in the above example, the error should be about the number of sides")


print()
print("### Example 12 ###")
try:
    class BeigeSquare(Filled, BetterPolygon):
        color = 'beige'
        sides = 4
except ValueError as ex:
    print(f"Error: {ex.args[0]}")


print()
print("### Example 12 ###")
class Top:
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"Top for {cls}")


class Left(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"Left for {cls}")


class Right(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"Right for {cls}")


class Bottom(Left, Right):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f"Bottom for {cls}")

"""
Top.__init_subclass__ is called only a single time for each class, even though
there are two paths to it for the Bottom class through its Left and Right
parent classes
"""
