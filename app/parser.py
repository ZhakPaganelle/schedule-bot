"""Parser for origin schedule website"""
import re
import requests
from bs4 import BeautifulSoup

LessonInfo = list[dict[str | int, int | str]]
DayInfo = dict[int, LessonInfo]
WeekInfo = dict[str, DayInfo]

HEADERS = {
    'x-requested-with': 'XMLHttpRequest',
}


def get_options(name: str, data: dict[str, str]) -> list[str]:
    """Requests page and returns all options' values from
    the selector with given name"""
    url = 'https://rasp.rea.ru/Schedule/Navigator'
    req = requests.post(url=url, headers=HEADERS, data=data)
    if req.status_code != 200:
        raise RuntimeError('Couldn\'t access the site')
    soup = BeautifulSoup(req.text, "html.parser")
    faculties = soup.find(attrs={"name": name})
    return [
        option['value'] for option in faculties.find_all('option')
        if option['value'] not in ('na', '')
    ]


def get_faculties() -> list[str]:
    """Returns list of all faculties"""
    data = {
        'ChangedNode': 'Faculty',
    }
    name = 'Faculty'
    return get_options(name, data)


def get_cathedras() -> list[str]:
    """Returns list of all cathedras"""
    data = {
        'ChangedNode': 'Cathedra',
    }
    name = 'Cathedra'
    return get_options(name, data)


def get_courses(faculty: str) -> list[str]:
    """Returns list of courses based on faculty"""
    data = {
        'Faculty': faculty,
        'ChangedNode': 'Faculty',
    }
    name = 'Course'
    return get_options(name, data)


def get_study_types(faculty: str, course: str = '1-й курс') -> list[str]:
    """Returns type of study (bachelor, master or specialist"""
    data = {
        'Faculty': faculty,
        'Course': course,
        'ChangedNode': 'Course',
    }
    name = 'Type'
    return get_options(name, data)


def get_groups(faculty: str, course: str, study_type: str) -> list[str]:
    """Returns list of groups from course
    based on faculty, year and studying type"""
    data = {
        'Faculty': faculty,
        'Course': course,
        'Type': study_type,
        'ChangedNode': 'Type',
    }
    name = 'Group'
    return get_options(name, data)


def get_schedule(group: str, week_num: int = -1, detailed: bool = False) -> list[dict[str | int, int | str]]:
    """Returns list of days with lessons
    Every day is also a list"""
    pass


def get_lesson_info(group: str, date: str, time_slot: int) -> LessonInfo:
    params = {'selection': group.lower(), 'date': date, 'timeSlot': time_slot}
    req = requests.get('https://rasp.rea.ru/Schedule/GetDetails', headers=HEADERS, params=params)  # type: ignore
    soup = BeautifulSoup(req.text, "html.parser")
    lessons = [div for div in soup.find_all('div') if div.attrs.get('data-subgroup')]

    subjects = [lesson.find('h5').text for lesson in lessons]

    types = [lesson.find('strong').text for lesson in lessons]

    rooms = [re.findall(r'Аудитория:\s+(\d+) \w+ -\s+(\d+)\s', str(lesson))[0] for lesson in lessons]
    teachers = [re.findall(r'</i> ([\w ]+)</a>', str(lesson)) for lesson in lessons]
    groups = [re.findall(r'Группа\s+([\w\./\- \d\(\)]+)\s+<br/>', str(lesson))[0] for lesson in lessons]

    contents = zip(subjects, types, rooms, teachers, groups)
    headings = ('subject', 'type', 'room', 'teachers', 'subgroup')
    return [dict(zip(headings, lesson)) for lesson in contents]  # type: ignore


if __name__ == '__main__':
    print(get_lesson_info('15.06д-э03а/19б', '26.04.2022', 5))
