"""Parser for origin schedule website"""
import re
import requests
from bs4 import BeautifulSoup

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
    week_schedule_req = requests.get(
        f'https://rasp.rea.ru/Schedule/ScheduleCard?selection={group}&weekNum={week_num}&catfilter=1',
        headers=HEADERS
    )
    week_schedule = BeautifulSoup(week_schedule_req.text, "html.parser")
    days = week_schedule.find_all('table')
    days_info = [get_day_info(day, detailed) for day in days]
    return days_info


def get_day_info(day, detailed: bool = False) -> dict[str | int, int | str]:
    day_info = {}
    date = day.find('h5').text
    day_info['day_of_the_week'], day_info['date'] = date.split(', ')
    lessons = day.find_all('tr')[1:]

    # Default empty dictionaries for empty lessons
    if detailed:
        for i in range(1, 9):
            day_info[i] = {}

    for i, lesson in enumerate(lessons, 1):
        day_info[i] = parse_lesson(lesson, detailed)
    return day_info


def parse_lesson(lesson, detailed: bool = False) -> dict[str | int, int | str]:
    cells = lesson.find_all('td')
    if len(cells) < 2 or not cells[1]:
        return {}
    subj_info = ' '.join(
        [string.strip() if isinstance(string, str)
         else ' '.join([str(elem) for elem in string.contents])
         for string in cells[1].contents]
    )
    subj_info = re.sub(r'\s+', ' ', subj_info)
    subj_info = re.sub(r'<br/>', '\n', subj_info)
    subj_info = re.sub(r'\s+', ' ', subj_info)
    print(1, subj_info)
    # keys = ['name', 'lesson_type', 'building', 'room', 'platform']
    # return dict(zip(keys, subj_info))
    return {}


if __name__ == '__main__':
    print(get_schedule('15.06д-э03а/19б'))
