class Preferences:
    __slots__ = ('start_time', 'end_time', 'rooms')

    def __init__(self, start_time=None, end_time=None, rooms=None):
        if rooms is None:
            rooms = list()
        self.start_time = start_time
        self.end_time = end_time
        self.rooms = rooms

    @property
    def time_preferences(self):
        return not (self.start_time is None and self.end_time is None)

    @property
    def room_preferences(self):
        return self.rooms


class Instructor:
    __slots__ = ('instructor_id', 'instructor_name', 'preferences')

    def __init__(self, instructor_id, instructor_name, preferences):
        if preferences is None:
            preferences = {'start_time': None, 'end_time': None}
        self.instructor_id = instructor_id
        self.instructor_name = instructor_name
        self.preferences = Preferences(**preferences)


class Instructors:
    __slots__ = ('primary', 'secondary')

    def __init__(self, primary, secondary=None):
        self.primary = Instructor(**primary)
        if secondary is not None:
            self.secondary = Instructor(**secondary)


class Subject:
    __slots__ = (
            '__cohort',
            '__id',
            '__title',
            '__instructors',
            '__duration',
            '__required_rooms',
            '__subject_status'
    )

    def __init__(self, cohort: int | str, id: int | str, title: str, instructors: dict, duration: int):
        self.__cohort = cohort
        self.__id = id
        self.__title = title
        self.__instructors = Instructors(**instructors)
        self.__duration = duration
        self.__required_rooms = None
        self.__subject_status = True

    @property
    def unique_id(self):
        return f'{self.__cohort}-{self.__id}:{self.__title}'

    @property
    def cohort(self):
        return self.__cohort

    @property
    def id_(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def instructors(self):
        return self.__instructors

    @property
    def duration(self):
        return self.__duration

    @property
    def subject_status(self):
        return self.__subject_status

    @subject_status.setter
    def subject_status(self, status: bool):
        self.__subject_status = status

    @property
    def required_rooms(self):
        return self.__required_rooms

    @required_rooms.setter
    def required_rooms(self, rooms):
        self.__required_rooms = rooms

    @property
    def update_me_later(self):
        return f'{self.__cohort}: {self.__title}'

    def __str__(self):
        return f'{self.unique_id}'

    def __repr__(self):
        return f'{self.unique_id}'
        # return f'Subject(id={self.__id}, title={self.__title}, cohort={self.__cohort})'


class Lecture(Subject):

    def __init__(self, cohort, id, title, instructors, duration):
        super().__init__(cohort=cohort, id=id, title=title, instructors=instructors, duration=duration)

    def __str__(self):
        return self.update_me_later

    def __repr__(self):
        return f'Lecture(subject_id={self.unique_id}'


class Tutorial(Subject):

    def __init__(self, cohort, id, title, instructors, duration):
        super().__init__(cohort=cohort, id=id, title=title, instructors=instructors, duration=duration)

    def __str__(self):
        return self.update_me_later

    def __repr__(self):
        return f'Tutorial(subject_id={self.unique_id}'


class Laboratory(Subject):

    def __init__(self, cohort, id, title, instructors, duration):
        super().__init__(cohort=cohort, id=id, title=title, instructors=instructors, duration=duration)

    def __str__(self):
        return self.update_me_later

    def __repr__(self):
        return f'Lecture(subject_id={self.unique_id}'


def get_subject(subject_type, cohort, id, title, instructors, duration):
    if subject_type == 'lecture':
        return Lecture(cohort=cohort, id=id, title=title, instructors=instructors, duration=duration)
    if subject_type == 'tutorial':
        return Tutorial(cohort=cohort, id=id, title=title, instructors=instructors, duration=duration)
    if subject_type == 'laboratory':
        return Laboratory(cohort=cohort, id=id, title=title, instructors=instructors, duration=duration)
