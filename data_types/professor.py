from typing import List


class Professor:

    def __new__(cls, *args, **kwargs):
        pass

    def __init__(self, name):
        self.__name: str = name
        self.__subjects: List[dict] = []