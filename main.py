from converter import Converter
from back_traking.subject import Subject


def main():
    converter = Converter()
    subjects = converter.xlsx_to_json()
    for subject in subjects:
        print(subject)
        _subject = Subject(**subject)
        print(_subject.instructor.primary.instructor_name)
        break


if __name__ == '__main__':
    main()
