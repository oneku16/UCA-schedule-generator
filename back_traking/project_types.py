from exceptions import ExceptionNoClasses, ExceptionClassLimit

class SubjectPattern:
    __slots__ = '_number_of_classes', '_duration', '_initial_number_of_classes'

    def __init__(self, number_of_classes, duration=90):
        self._number_of_classes = number_of_classes
        self._duration = duration
        self._initial_number_of_classes = duration

    @property
    def is_possible(self):
        return not self._number_of_classes

    @property
    def number_of_classes(self):
        return self._number_of_classes

    @property
    def duration(self):
        return self._duration

    def set_class(self):
        if self.is_possible:
            raise ExceptionNoClasses
        self._number_of_classes -= 1

    def add_class(self):
        if self.number_of_classes == self._initial_number_of_classes:
            raise ExceptionClassLimit
        self._number_of_classes += 1


class Lecture:
    __slots__ = '_lecture'

    def __init__(self, number_of_lectures, duration):
        self._lecture = SubjectPattern(number_of_lectures, duration)

    @property
    def lecture(self):
        return self._lecture


class LectureTutorial(Lecture):
    __slots__ = '_tutorial'

    def __init__(self, number_of_lectures, lecture_duration, number_of_tutorials, tutorial_duration):
        self._tutorial = SubjectPattern(number_of_tutorials, tutorial_duration)
        super().__init__(number_of_lectures, lecture_duration)

    @property
    def tutorial(self):
        return self._tutorial


class LectureTutorialLaboratory(LectureTutorial):
    __slots__ = '_laboratory'

    def __init__(self, number_of_lectures, lecture_duration, number_of_tutorials, tutorial_duration, number_of_laboratories, laboratory_duration):
        super().__init__(number_of_lectures, lecture_duration, number_of_tutorials, tutorial_duration)
        self._laboratory = SubjectPattern(number_of_laboratories, laboratory_duration)

    @property
    def laboratory(self):
        return self._laboratory




