from .intructor_type import InstructorType

class Instructor:
    __slots__ = '_primary', '_secondary'

    def __init__(self, primary, secondary=None):
        if secondary is None:
            secondary = {'instructor_name': None}
        self._primary = InstructorType(**primary)
        self._secondary = InstructorType(**secondary)

    @property
    def primary(self):
        return self._primary

    @property
    def secondary(self):
        return self._secondary
