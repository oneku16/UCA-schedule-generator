from converter import Converter


def main():
    converter = Converter()
    subjects = converter.xlsx_to_json()
    print(subjects)


if __name__ == '__main__':
    main()
