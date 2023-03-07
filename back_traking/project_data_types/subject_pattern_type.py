from back_traking.project_exceptions.subject_exceptions import ExceptionNoClasses, ExceptionClassLimit

class SubjectPatternType:
    __slots__ = '_classes', '_duration', '_initial_number_of_classes'

    def __init__(self, classes: (int | None), duration: int):
        self._classes = classes
        self._duration = duration
        self._initial_number_of_classes = duration

    @property
    def is_exist(self):
        return False if self._classes is None else True

    @property
    def _is_possible(self):
        return not self._classes

    @property
    def number_of_classes(self):
        return self._classes

    @property
    def duration(self):
        return self._duration

    def set_class(self):
        if self._is_possible:
            raise ExceptionNoClasses
        self._classes -= 1

    def add_class(self):
        if self.number_of_classes == self._initial_number_of_classes:
            raise ExceptionClassLimit
        self._classes += 1