from os import path

BASE_DIR = path.dirname(path.realpath(__file__))

DEANS_MEMO_PATH = "sources/Course Memo_Spring 2023_ver05_10.01.23_updated by Serik M.xlsx"

DEPARTMENT_NAMES = (
        "Preparatory",
        "Computer Science",
        "Communications & Media",
        "Earth & Environmental Sciences",
        "Economics")

SUBJECT_JSON = {
        'id': None,
        'title': None,
        'cohort': None,
        'patterns': None,
        'instructors': {
        }
}

SUBJECT_PATTERNS = ('lecture', 'tutorial', 'laboratory',)

DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',)
QUARTERS = (1, 2, 3, 4)

ROOMS = (
        {'room_id': '201', 'capacity': 25, 'room_type': 'lecture', 'room_name': 'Red classroom'},
        {'room_id': '202', 'capacity': 25, 'room_type': 'lecture', 'room_name': 'White classroom'},
        {'room_id': '203', 'capacity': 25, 'room_type': 'lecture', 'room_name': 'Grey classroom'},
        {'room_id': '204', 'capacity': 25, 'room_type': 'lecture', 'room_name': 'Green classroom'},
        {'room_id': '206', 'capacity': 25, 'room_type': 'laboratory', 'room_name': 'Dry laboratory'},
        {'room_id': '209', 'capacity': 25, 'room_type': 'lecture', 'room_name': 'Yellow classroom'},
        {'room_id': '109', 'capacity': 25, 'room_type': 'laboratory', 'room_name': 'Wet laboratory '},
        {'room_id': '111', 'capacity': 25, 'room_type': 'laboratory', 'room_name': 'IT Laboratory '},
        {'room_id': '-14', 'capacity': 25, 'room_type': 'laboratory', 'room_name': 'Communication and Media lab'},
        {'room_id': '328', 'capacity': 25, 'room_type': 'laboratory', 'room_name': 'Hardware laboratory'},
        {'room_id': '104', 'capacity': 25, 'room_type': 'lecture', 'room_name': 'Creative room'},
        {'room_id': '100', 'capacity': 100, 'room_type': 'physical_training', 'room_name': 'Sport Bubble'}
)

SLOTS = (
        {'hour': '09', 'minute': '00', 'duration': 90},
        {'hour': '11', 'minute': '00', 'duration': 90},
        {'hour': '14', 'minute': '00', 'duration': 90},
        {'hour': '16', 'minute': '00', 'duration': 90}
)

PRIORITY = {
        'right_slot': 1,
        'left_slot': 0,
        'subjects_in_days': 2,
        'subjects_in_quarter': 3,
}

ROOM_COLOR = {'201': 'FF0000',
              '202': 'FFFFFF',
              '203': 'D0CECE',
              '204': '92D050',
              '206': 'CC99FF',
              '209': 'FFFF00',
              '109': 'F8CBAD',
              '111': 'F4B084',
              '3.28': 'D6DCE4',
              'B14': '8EA9DB',
              '11': '00FFFF',
              '69': 'FFFFFF'}
