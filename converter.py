from openpyxl import load_workbook, Workbook
from config import DEANS_MEMO_PATH, DEPARTMENT_NAMES
from typing import List


class Converter:
    __slots__ = ('xlsx_file', 'main_data')

    def __init__(self):
        self.xlsx_file = load_workbook(DEANS_MEMO_PATH, data_only=True)
        self.main_data = List[dict]

    def get_xlsx_sheet(self, sheet_name: int | str) -> object:
        try:
            if type(sheet_name) is int:
                return self.xlsx_file[self.xlsx_file.sheetnames[sheet_name]]
            return self.xlsx_file[sheet_name]
        except KeyError:
            if type(sheet_name) is int:
                raise "xlsx sheet list index out of range"

    def xlsx_to_json(self, sheet_name='Spring 2023'):
        local_sheet = self.get_xlsx_sheet(sheet_name)
        properties = [cell.value for cell in local_sheet[1]]
        cohort = None

        for index in range(2, local_sheet.max_row + 1):
            row = [cell.value for cell in local_sheet[index]]
            if row[0] in DEPARTMENT_NAMES:
                cohort = row[0]
                print(cohort)
