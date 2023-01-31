from typing import List, DefaultDict


class Mutation:
    __slots__ = ('generation', 'current', 'properties')

    def __new__(cls, *args, **kwargs): ...

    def __init__(self):
        self.generation = DefaultDict
        self.current = None
        self.properties = List[dict]
