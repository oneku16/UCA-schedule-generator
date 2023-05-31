class Slot:
    __slots__ = ('__slots', '__stack')

    class _Quarter:
        __slots__ = ('__status', '__subject')

        def __init__(self, status: bool = True, subject: object = None):
            self.__status: bool = status
            self.__subject: object = subject

        @property
        def status(self) -> bool:
            return self.__status

        @property
        def subject(self) -> object:
            return self.__subject

        @status.setter
        def status(self, new_status: bool):
            self.__status = new_status

        @subject.setter
        def subject(self, new_subject: object):
            self.__subject = new_subject

    def __init__(self):
        self.__slots = {number: self._Quarter() for number in (1, 2, 3, 4)}

    def is_possible(self, subject: object) -> bool:
        ...
