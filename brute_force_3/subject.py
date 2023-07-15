class Subject:
    __slots__ = (
            '__cohort',
            '__id',
            '__title',
            '__instructors',
            '__subject_type',
            '__duration',
            '__required_rooms',
            '__subject_status'
    )

    def __init__(self, cohort, id, title, instructors, subject_type, duration):
        self.__cohort = cohort
        self.__id = id
        self.__title = title
        self.__instructors = instructors
        self.__subject_type = subject_type
        self.__duration = duration
        self.__required_rooms = None
        self.__subject_status = True

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
    def subject_type(self):
        return self.__subject_type

    @property
    def duration(self):
        return self.__duration

    @property
    def subject_status(self):
        return self.__subject_status

    @subject_status.setter
    def subject_status(self, status: bool):
        self.__subject_status = status

    def __str__(self):
        return f'{self.__title}'

    def __repr__(self):
        return f'Subject(id={self.__id}, title={self.__title}, cohort={self.__cohort})'
