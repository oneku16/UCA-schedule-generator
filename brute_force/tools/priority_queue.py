from heapq import heappop, heappush, heappushpop, heapify
from typing import Generator
from brute_force.subject.subject import Subject


class HeapQ:
    __slots__ = '__collections'

    def __init__(self):
        self.__collections = []

    def add(self, order, value) -> None:
        # print(*order, value)
        temp = (*order, value)
        print(temp)
        heappush(self.__collections, temp)

    def get(self) -> Subject:
        return heappop(self.__collections)[-1]

    def __iter__(self) -> Generator[Subject, None, None]:
        for item in self.__collections:
            yield item

    def __len__(self) -> int:
        return len(self.__collections)

    def __repr__(self):
        return ' '.join(map(str, [item[-1].title for item in self.__collections]))
