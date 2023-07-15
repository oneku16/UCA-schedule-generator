from typing import Dict


class Instructor:
    __slots__ = ('__instructor_id', '__instructor_name', '__preferences')

    def __init__(self, instructor_id, instructor_name, preferences):
        self.__instructor_id = instructor_id
        self.__instructor_name = instructor_name
        self.__preferences = preferences

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
    __slots__ = ('__primary', '__secondary',)

    def __init__(self, primary: Dict, secondary: Dict = None):
        self.__primary = Instructor(**primary)
        self.__secondary = Instructor(**secondary) or None

    @property
    def primary(self):
        return self.__primary

    @property
    def secondary(self):
        return self.__secondary


