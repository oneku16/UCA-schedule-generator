from back_traking.project_exceptions.subject_exceptions import ExceptionNoClasses, ExceptionClassLimit


class SubjectPatternType:
    __slots__ = '_name', '_number_of_classes', '_class_duration', '_initial_number_of_classes'

    def __init__(self, name, pattern):
        self._name = name
        self._number_of_classes, self._class_duration = pattern
        self._initial_number_of_classes = self._number_of_classes

    @property
    def name(self):
        return self._name

    @property
    def number_of_classes(self):
        return self._number_of_classes

    @property
    def class_duration(self):
        return self._class_duration

    def is_possible(self, add=False):
        if add:
            return 0 <= self._number_of_classes < self._initial_number_of_classes
        return self._number_of_classes >= 1

    def reserve_class(self):
        if not self.is_possible():
            raise ExceptionNoClasses
        self._number_of_classes -= 1

    def undo_reservation(self):
        if not self.is_possible(add=True):
            raise ExceptionClassLimit
        self._number_of_classes += 1
