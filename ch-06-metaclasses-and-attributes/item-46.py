from weakref import WeakKeyDictionary


class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not(0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100'
            )
        self._value = value

class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)

# But accessing these attributes on multiple Exam instances causes unexpected
# behavior

second_exam = Exam()
second_exam.writing_grade = 72
print(f"Second {second_exam.writing_grade} is right" )
print(f"First {first_exam.writing_grade} is wrong, should be 82" )

#  What's happening here? A single Grade instance is shared across all Exam instances
#  We need to construct a Grade class that can keep track of its value for each Exam instance

class GradeImproved:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100'
            )
        self._values[instance] = value


class Exam2:
    math_grade = GradeImproved()
    writing_grade = GradeImproved()
    science_grade = GradeImproved()


first_exam = Exam2()
first_exam.writing_grade = 82
second_exam = Exam2()
second_exam.writing_grade = 75

print(f"First {first_exam.writing_grade} is OK")
print(f"Second {second_exam.writing_grade} is OK")
