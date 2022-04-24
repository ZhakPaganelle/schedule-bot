"""Parser for origin schedule website"""
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
