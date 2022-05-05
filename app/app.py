"""Parsed API from rasp.rea.ru"""
from fastapi import FastAPI, responses
from starlette import status

from app import schedule_parser

application = FastAPI()


@application.get("/hello/", response_model=str)
async def hello():
    """Test function"""
    return "Hello"


@application.get("/api/faculties/")
async def get_faculties():
    """Returns json with list of faculties"""
    return await schedule_parser.get_faculties()


@application.get("/api/faculties/{faculty}")
async def get_courses(faculty: str):
    """Returns json with years for current faculty"""
    return await schedule_parser.get_courses(faculty)


@application.get("/api/faculties/{faculty}/{course}")
async def get_types(faculty: str, course: str):
    """Returns are there any bachelors/masters/specialist in current course"""
    return await schedule_parser.get_study_types(faculty, course)


@application.get("/api/faculties/{faculty}/{course}/{study_type}")
async def get_groups(faculty: str, course: str, study_type: str):
    """Returns groups from given faculty, course and type of studying"""
    return await schedule_parser.get_groups(faculty, course, study_type)


@application.get("/api/faculties/{faculty}/{course}/{study_type}/{group:path}")
async def redirect_to_group_schedule(group: str):
    """Redirects user to schedule of given group"""
    return responses.RedirectResponse(
        f'/api/schedule/{group}',
        status_code=status.HTTP_302_FOUND)


@application.get("/api/cathedras/")
async def get_cathedras():
    """Returns list of cathedras"""
    return await schedule_parser.get_cathedras()


@application.get("/api/cathedras/{cathedra}")
async def get_teachers(cathedra: str):
    """Returns list of teachers on given cathedra"""
    return await schedule_parser.get_teachers(cathedra)


@application.get("/api/cathedras/{cathedra}/{teacher}")
async def redirect_to_teacher_schedule(teacher: str):
    """Redirects user to schedule of given teacher"""
    return responses.RedirectResponse(
        f'/api/schedule/{teacher}',
        status_code=status.HTTP_302_FOUND)


@application.get('/api/schedule/{selection:path}/date/{date:str}')
async def send_schedule_date(selection: str, date: str):
    """Returns all lessons on a given date"""
    return await schedule_parser.get_day_info(selection, date)


@application.get('/api/schedule/{selection:path}/date/{date:str}/lesson/{lesson_id}')
async def send_lesson_by_date(selection: str, date: str, lesson_id: int):
    """Returns info about given lesson"""
    return await schedule_parser.get_lesson_info(selection, date, lesson_id)


@application.get('/api/schedule/{selection:path}/week/{week_num}/day/{day_num:int}')
async def send_schedule_day_by_week(selection: str, week_num: int, day_num: int):
    """Returns all lessons on a given day of the week (starting from 1)"""
    selection = selection.lower()
    dates = await schedule_parser.get_dates(selection, week_num)
    date = dates[day_num - 1]
    return await schedule_parser.get_day_info(selection, date)


@application.get('/api/schedule/{selection:path}/week/{week_num}')
async def send_schedule_week(selection: str, week_num: int):
    """Returns all lessons on a given week"""
    return await schedule_parser.get_week_info(selection.lower(), int(week_num))


@application.get('/api/schedule/{selection:path}/week/{week_num}/day/{day_num}/lesson/{lesson_id}')
async def send_lesson_by_week(selection: str, week_num: int, day_num: int, lesson_id: int):
    """Returns all lessons on a given day of the week (days starting from 1)"""
    dates = await schedule_parser.get_dates(selection, week_num)
    date = dates[day_num - 1]
    return await schedule_parser.get_lesson_info(selection, date, lesson_id)


@application.get('/api/schedule/{selection:path}')
async def send_schedule(selection: str):
    """Returns all lessons on current week"""
    return await schedule_parser.get_week_info(selection)
