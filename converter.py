from openpyxl import load_workbook
from config import DEANS_MEMO_PATH, DEPARTMENT_NAMES, SUBJECT_JSON
from typing import List, Any, Tuple
from copy import deepcopy


class Converter:
    __slots__ = 'xlsx_file', '_TBD'

    class __TBD:
        _index = 0

        @property
        def index(self):
            self._index += 1
            return f'TBD{self._index}'

    def __init__(self):
        self.xlsx_file = load_workbook(DEANS_MEMO_PATH, data_only=True)
        self._TBD = self.__TBD()

    def get_xlsx_sheet(self, sheet_name: int | str) -> object:
        try:
            if type(sheet_name) is int:
                return self.xlsx_file[self.xlsx_file.sheetnames[sheet_name]]
            return self.xlsx_file[sheet_name]
        except KeyError:
            if type(sheet_name) is int:
                raise "xlsx sheet list index out of range"

    @staticmethod
    def get_subject_id(subject_area, course_code) -> str:
        return f'{str(subject_area).strip()}{str(course_code).strip()}'.strip()

    @staticmethod
    def get_subject_title(subject_title: str) -> str:
        return subject_title.replace(u'\xa0', u' ').strip()

    def set_subject_type(self, subject_patterns) -> tuple[dict, ...]:

        def _wrapper():
            for subject_pattern in self.get_subject_patterns(subject_patterns):
                yield subject_pattern

        return list(_wrapper())

    @staticmethod
    def get_subject_patterns(course_types: str) -> List[dict]:
        def _splitter():
            try:
                for subject_pattern in course_types.split(','):
                    subject_pattern = list(int(item.strip()) for item in subject_pattern.split('x'))
                    yield {'classes': subject_pattern[0], 'duration': subject_pattern[1]}
            except AttributeError:
                return [course_types]

        return list(_splitter())

    @staticmethod
    def distribute_by_cohort(undergraduate_year, cohort, cohort_number=None) -> str:
        if cohort_number:
            return f'Group {cohort_number[0]} {cohort}'.strip()
        return f'{"".join(map(str, filter(str.isupper, undergraduate_year)))} {cohort}'.strip()

    def get_instructor_names(self, primary_instructor: str, secondary_instructor: str | None) -> dict:
        if primary_instructor:
            if primary_instructor.strip() == 'TBD':
                return {'primary': {'instructor_id': None, 'instructor_name': self._TBD.index, 'preferences': None}}
            instructors = {'primary': {'instructor_id': None, 'instructor_name': primary_instructor.strip(), 'preferences': None}}
            if secondary_instructor:
                instructors['secondary'] = {'instructor_id': None, 'instructor_name': secondary_instructor.strip(), 'preferences': None}
            return instructors
        return {'primary': {'instructor_id': None, 'instructor_name': self._TBD.index, 'preferences': None}}

    def xlsx_to_json(self, sheet_name='Spring 2023'):
        def _wrapper():

            sheet = self.get_xlsx_sheet(sheet_name)
            cohort = None
            for index in range(2, sheet.max_row + 1):

                subject_json = deepcopy(SUBJECT_JSON)

                if sheet[f'A{index}'].value in DEPARTMENT_NAMES:
                    cohort = sheet[f'A{index}'].value
                    continue
                if sheet[f'A{index}'].value and sheet[f'B{index}'].value:
                    subject_json['id'] = self.get_subject_id(sheet[f'A{index}'].value, sheet[f'B{index}'].value)
                if sheet[f'C{index}'].value:
                    subject_json['title'] = self.get_subject_title(sheet[f'C{index}'].value)
                if sheet[f'G{index}'].value:
                    subject_json['cohort'] = self.distribute_by_cohort(cohort, sheet[f'G{index}'].value,
                                                                       sheet[f'I{index}'].value)
                if sheet[f'L{index}'].value:
                    subject_json['patterns'] = self.set_subject_type(sheet[f'L{index}'].value)
                subject_json['instructors'] = self.get_instructor_names(sheet[f'M{index}'].value, sheet[f'N{index}'].value)
                yield subject_json

        return list(_wrapper())
