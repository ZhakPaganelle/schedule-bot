"""Parser for origin schedule website"""
import re
import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup

LessonInfo = list[dict[str | int, int | str]]
DayInfo = dict[int, LessonInfo]
WeekInfo = dict[str, DayInfo]

HEADERS = {
    'x-requested-with': 'XMLHttpRequest',
}


async def get_options(name: str, data: dict[str, str]) -> list[str]:
    """Requests page and returns all options' values from
    the selector with given name"""
    url = 'https://rasp.rea.ru/Schedule/Navigator'
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=HEADERS, data=data) as req:
            if req.status != 200:
                raise RuntimeError('Couldn\'t access the site')
            text = await req.text()
            soup = BeautifulSoup(text, "html.parser")
            faculties = soup.find(attrs={"name": name})
            return [
                option['value'] for option in faculties.find_all('option')
                if option['value'] not in ('na', '')
            ]


async def get_faculties() -> list[str]:
    """Returns list of all faculties"""
    data = {
        'ChangedNode': 'Faculty',
    }
    name = 'Faculty'
    return await get_options(name, data)


async def get_cathedras() -> list[str]:
    """Returns list of all cathedras"""
    data = {
        'ChangedNode': 'Cathedra',
    }
    name = 'Cathedra'
    return await get_options(name, data)


async def get_courses(faculty: str) -> list[str]:
    """Returns list of courses based on faculty"""
    data = {
        'Faculty': faculty,
        'ChangedNode': 'Faculty',
    }
    name = 'Course'
    return await get_options(name, data)


async def get_study_types(faculty: str, course: str = '1-й курс') -> list[str]:
    """Returns type of study (bachelor, master or specialist"""
    data = {
        'Faculty': faculty,
        'Course': course,
        'ChangedNode': 'Course',
    }
    name = 'Type'
    return await get_options(name, data)


async def get_groups(faculty: str, course: str, study_type: str) -> list[str]:
    """Returns list of groups from course
    based on faculty, year and studying type"""
    data = {
        'Faculty': faculty,
        'Course': course,
        'Type': study_type,
        'ChangedNode': 'Type',
    }
    name = 'Group'
    return await get_options(name, data)


async def get_lesson_info(selection: str, date: str, time_slot: int) -> LessonInfo:
    url = 'https://rasp.rea.ru/Schedule/GetDetails'
    params = {'selection': selection.lower(), 'date': date, 'timeSlot': time_slot}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS, params=params) as req:
            soup = BeautifulSoup(await req.text(), "html.parser")

    lessons = [div for div in soup.find_all('div') if div.attrs.get('data-subgroup')]

    subjects = [lesson.find('h5').text for lesson in lessons]

    types = [lesson.find('strong').text for lesson in lessons]

    rooms_raw = [re.findall(r'Аудитория:\s+(\d+) \w+ -\s+(\d+)\s', str(lesson)) for lesson in lessons]
    rooms = [room[0] if room else room for room in rooms_raw]
    teachers = [re.findall(r'</i> ([\w ]+)</a>', str(lesson)) for lesson in lessons]
    groups_raw = [re.findall(r'Группа\s+([\w\./\- \d\(\)]+)\s+<br/>', str(lesson)) for lesson in lessons]
    groups = [group[0] if group else group for group in groups_raw]

    contents = zip(subjects, types, rooms, teachers, groups)
    headings = ('subject', 'type', 'room', 'teachers', 'group')
    return [dict(zip(headings, lesson)) for lesson in contents]  # type: ignore


async def get_day_info(selection: str, date: str) -> DayInfo:
    lessons = asyncio.gather(*[get_lesson_info(selection, date, lesson_index) for lesson_index in range(1, 9)])
    return dict(zip(range(1, 9), await lessons))


async def get_week_info(selection: str, week_num: int = -1) -> WeekInfo:
    dates = await get_dates(selection, week_num)
    days = asyncio.gather(*[get_day_info(selection, date) for date in dates])
    return dict(zip(dates, await days))


async def get_dates(selection: str, week_num: int = -1) -> set[str]:
    url = 'https://rasp.rea.ru/Schedule/ScheduleCard'
    params = {'selection': selection.lower(), 'weekNum': week_num}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS, params=params) as schedule:
            return set(re.findall(r'\d{2}\.\d{2}\.\d{4}', await schedule.text()))
