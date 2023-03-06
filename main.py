from converter import Converter
from back_traking.subject import Subject
from back_traking.project_types import SubjectPattern


def main():
    # converter = Converter()
    # subjects = converter.xlsx_to_json()
    # # for subject in subjects:
    # #     print(subject)
    # for subject in subjects:
    #     # print(subject)
    #     _subject = Subject(**subject)
    #     print(_subject.get_lecture(), _subject.get_tutorial(), _subject.get_laboratory(), _subject.get_subject_name())
    s = SubjectPattern(1, 1)
    print(s.a)

if __name__ == '__main__':
    main()
