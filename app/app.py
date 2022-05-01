"""Parsed API from rasp.rea.ru"""
from fastapi import FastAPI, responses
from starlette import status

from app import schedule_parser

application = FastAPI()


@application.get("/hello/", response_model=str)
async def hello():
    """Test function"""
    return "Hello2"


@application.get("/api/faculties/")
async def get_faculties():
    return await schedule_parser.get_faculties()


@application.get("/api/faculties/{faculty}")
async def get_courses(faculty: str):
    return await schedule_parser.get_courses(faculty)


@application.get("/api/faculties/{faculty}/{course}")
async def get_types(faculty: str, course: str):
    return await schedule_parser.get_study_types(faculty, course)


@application.get("/api/faculties/{faculty}/{course}/{study_type}")
async def get_groups(faculty: str, course: str, study_type: str):
    return await schedule_parser.get_groups(faculty, course, study_type)


@application.get("/api/faculties/{faculty}/{course}/{study_type}/{group:path}")
async def redirect_to_group_schedule(group: str):
    return responses.RedirectResponse(
        f'/api/schedule/{group}',
        status_code=status.HTTP_302_FOUND)


@application.get("/api/cathedras/")
async def get_cathedras():
    return await schedule_parser.get_cathedras()


@application.get("/api/cathedras/{cathedra}")
async def get_teachers(cathedra: str):
    return await schedule_parser.get_teachers(cathedra)


@application.get("/api/cathedras/{cathedra}/{teacher}")
async def redirect_to_teacher_schedule(teacher: str):
    return responses.RedirectResponse(
        f'/api/schedule/{teacher}',
        status_code=status.HTTP_302_FOUND)


@application.get('/api/schedule/{selection:path}/date/{date:str}')
async def send_schedule_date(selection: str, date: str):
    return await schedule_parser.get_day_info(selection, date)


@application.get('/api/schedule/{selection:path}/date/{date:str}/lesson/{lesson_id}')
async def send_lesson_by_date(selection: str, date: str, lesson_id: int):
    return await schedule_parser.get_lesson_info(selection, date, lesson_id)


@application.get('/api/schedule/{selection:path}/week/{week_num}/day/{day_num:int}')
async def send_schedule_day_by_week(selection: str, week_num: int, day_num: int):
    selection = selection.lower()
    dates = await schedule_parser.get_dates(selection, week_num)
    date = dates[day_num - 1]
    return await schedule_parser.get_day_info(selection, date)


@application.get('/api/schedule/{selection:path}/week/{week_num}')
async def send_schedule_week(selection: str, week_num: int):
    return await schedule_parser.get_week_info(selection.lower(), int(week_num))


@application.get('/api/schedule/{selection:path}/week/{week_num}/day/{day_num}/lesson/{lesson_id}')
async def send_lesson_by_week(selection: str, week_num: int, day_num: int, lesson_id: int):
    dates = await schedule_parser.get_dates(selection, week_num)
    date = dates[day_num - 1]
    return await schedule_parser.get_lesson_info(selection, date, lesson_id)


@application.get('/api/schedule/{selection:path}')
async def send_schedule(selection: str):
    return await schedule_parser.get_week_info(selection)
