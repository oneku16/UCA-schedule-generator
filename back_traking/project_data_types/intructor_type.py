class InstructorType:
    __slots__ = '_instructor_id', '_instructor_name', '_preferences'

    def __init__(self, instructor_name, instructor_id=None, preferences=None):
        self._instructor_id = instructor_id
        self._instructor_name = instructor_name
        self._preferences = preferences

    @property
    def is_instructor_exist(self):
        return False if self._instructor_name is None else True

    @property
    def instructor_id(self):
        return self._instructor_id

    @property
    def instructor_name(self):
        return self._instructor_name

    @property
    def preferences(self):
        return self._preferences
