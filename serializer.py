from openpyxl import Workbook
from json import dump

class Serializer:
    __slots__ = '_file_name', '_path', '_schedule'

    def __init__(self):
        self._file_name = 'schedule'

    def to_json(self):
        ...

    def to_excel(self):
        ...
