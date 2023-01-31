from base import Base


class Converter(Base):

    def __init__(self):
        super().__init__()

    def get_xlsx(self):
        print(self.xlsx_file)

