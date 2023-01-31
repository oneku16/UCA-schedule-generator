from openpyxl import load_workbook, Workbook
from config import DEANS_MEMO_PATH


class Base:
    xlsx_file = None

    def read_xlsx(self) -> object:
        with open(DEANS_MEMO_PATH, 'rb') as file:
            self.xlsx_file = load_workbook(file, data_only=True)
        return self.xlsx_file
