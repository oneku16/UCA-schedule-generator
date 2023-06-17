class InstructorBuilder:
    __slots__ = ('__instructor_id', '__instructor_name', '__preferences')

    def __init__(self, *, instructor_id, instructor_name, preferences):
        self.__instructor_id = instructor_id
        self.__instructor_name = instructor_name
        self.__preferences = preferences

    def __str__(self):
        return self.__instructor_name

    @property
    def instructor_id(self):
        return self.__instructor_id

    @property
    def instructor_name(self):
        return self.__instructor_name

    @property
    def preferences(self):
        return self.__preferences


class Instructors:
    __slots__ = ('__primary', '__secondary')

    def __init__(self, *, primary=None, secondary=None):
        self.__primary = InstructorBuilder(**primary)
        self.__secondary = InstructorBuilder(**secondary) if secondary is not None else None

    @property
    def primary(self):
        return self.__primary

    @property
    def secondary(self):
        return self.__secondary
