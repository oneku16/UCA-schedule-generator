from converter import Converter
from back_traking.project_typing import Subject


def main():
    converter = Converter()
    subjects = converter.xlsx_to_json()
    for subject in subjects:
        _subject = Subject(**subject)
        print(_subject.get_subject_patterns())


if __name__ == '__main__':
    main()
