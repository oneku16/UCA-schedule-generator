from .subject_pattern_type import SubjectPatternType


class SubjectPattern:
    __slots__ = '_lecture', '_tutorial', '_laboratory'

    def __init__(self, lecture, tutorial=None, laboratory=None):
        if tutorial is None:
            tutorial = {'classes': None, 'duration': None}
        if laboratory is None:
            laboratory = {'classes': None, 'duration': None}
        self._lecture = SubjectPatternType(**lecture)
        self._tutorial = SubjectPatternType(**tutorial)
        self._laboratory = SubjectPatternType(**laboratory)

    @property
    def lecture(self):
        return self._lecture

    @property
    def tutorial(self):
        return self._tutorial

    @property
    def laboratory(self):
        return self._laboratory

    @property
    def is_lecture_exist(self):
        return self._lecture.is_exist

    @property
    def is_tutorial_exist(self):
        return self._lecture.is_exist

    @property
    def is_laboratory_exist(self):
        return self._laboratory.is_exist

    @property
    def number_of_lectures(self):
        return self._lecture.number_of_classes

    @property
    def number_of_tutorials(self):
        return self._tutorial.number_of_classes

    @property
    def number_of_laboratories(self):
        return self._laboratory.number_of_classes

    @property
    def duration_lecture(self):
        return self._lecture.duration

    @property
    def duration_tutorials(self):
        return self._tutorial.duration

    @property
    def duration_laboratory(self):
        return self._laboratory.duration

    def set_lecture(self):
        self._lecture.set_class()

    def set_tutorial(self):
        self._tutorial.set_class()

    def set_laboratory(self):
        self._laboratory.set_class()
