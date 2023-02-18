from openpyxl import load_workbook, Workbook
from config import DEANS_MEMO_PATH, DEPARTMENT_NAMES, COLUMNS, SUBJECT_JSON
from typing import List
from copy import deepcopy
from re import sub


class Converter:
    __slots__ = 'xlsx_file', 'main_data'

    def __init__(self):
        self.xlsx_file = load_workbook(DEANS_MEMO_PATH, data_only=True)
        self.main_data = []

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

    def set_subject_type(self, subject_types, subject_patterns) -> dict:
        subject_type = self.get_subject_types(subject_types)
        subject_patterns = self.get_subject_patterns(subject_patterns)
        # print(subject_types)
        # print(subject_patterns)
        return {None: None}

    @staticmethod
    def get_subject_types(subject_slots):
        if subject_slots:
            _bans = (',', 'and', ' ', '.')
            subject_slots = list(filter(lambda item: item not in _bans, sub(r'\W+', ' ', subject_slots).split()))
            return subject_slots
        return subject_slots

    @staticmethod
    def get_subject_patterns(course_types):
        try:
            course_types = course_types.split(',')
        except AttributeError:
            return [course_types]
        return course_types

    @staticmethod
    def distribute_by_cohort(undergraduate_year, cohort, cohort_number=None):
        if cohort_number:
            return f'Group {cohort_number[0]} {cohort}'.strip()
        return f'{"".join(map(str, filter(str.isupper, undergraduate_year)))} {cohort}'.strip()

    def is_valid_instructor(self, instructors):
        ...

    def xlsx_to_json(self, sheet_name='Spring 2023'):
        sheet = self.get_xlsx_sheet(sheet_name)
        cohort = None
        for index in range(2, sheet.max_row + 1):

            subject_json = deepcopy(SUBJECT_JSON)

            if sheet[f'A{index}'].value in DEPARTMENT_NAMES:
                cohort = sheet[f'A{index}'].value
                continue
            if sheet[f'A{index}'].value and sheet[f'B{index}'].value:
                subject_json['subject_id'] = self.get_subject_id(sheet[f'A{index}'].value, sheet[f'B{index}'].value)

            if sheet[f'C{index}'].value:
                subject_json['subject_name'] = sheet[f'C{index}'].value

            self.set_subject_type(sheet[f'J{index}'].value, sheet[f'L{index}'].value)

            subject_json['cohort'] = self.distribute_by_cohort(cohort, sheet[f'G{index}'].value, sheet[f'I{index}'].value)
            self.main_data.append(subject_json)
        for data in self.main_data:
            print(data)
