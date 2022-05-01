"""Parsed API from rasp.rea.ru"""
from fastapi import FastAPI, responses
import starlette.status as status

import parser

app = FastAPI()


@app.get("/hello/", response_model=str)
async def hello():
    """Test function"""
    return "Hello2"


@app.get("/api/faculties/")
async def get_faculties():
    return await parser.get_faculties()


@app.get("/api/faculties/{faculty}")
async def get_courses(faculty: str):
    return await parser.get_courses(faculty)


@app.get("/api/faculties/{faculty}/{course}")
async def get_types(faculty: str, course: str):
    return await parser.get_study_types(faculty, course)


@app.get("/api/faculties/{faculty}/{course}/{study_type}")
async def get_groups(faculty: str, course: str, study_type: str):
    return await parser.get_groups(faculty, course, study_type)


@app.get("/api/faculties/{faculty}/{course}/{study_type}/{group:path}")
async def redirect_to_group_schedule(faculty: str, course: str, study_type: str, group: str):  # type: ignore
    return responses.RedirectResponse(
        f'/api/schedule/{group}',
        status_code=status.HTTP_302_FOUND)


@app.get("/api/cathedras/")
async def get_cathedras():
    return await parser.get_cathedras()


@app.get("/api/cathedras/{cathedra}")
async def get_teachers(cathedra: str):
    return await parser.get_teachers(cathedra)


@app.get("/api/cathedras/{cathedra}/{teacher}")
async def redirect_to_teacher_schedule(cathedra: str, teacher: str):  # type: ignore
    return responses.RedirectResponse(
        f'/api/schedule/{teacher}',
        status_code=status.HTTP_302_FOUND)


@app.get('/api/schedule/{selection:path}/date/{date:str}')
async def send_schedule_date(selection: str, date: str):
    return await parser.get_day_info(selection, date)


@app.get('/api/schedule/{selection:path}/date/{date:str}/lesson/{lesson_id}')
async def send_lesson_by_date(selection: str, date: str, lesson_id: int):
    return await parser.get_lesson_info(selection, date, lesson_id)


@app.get('/api/schedule/{selection:path}/week/{week_num}/day/{day_num:int}')
async def send_schedule_week(selection: str, week_num: int, day_num: int):
    selection = selection.lower()
    dates = await parser.get_dates(selection, week_num)
    date = dates[day_num - 1]
    return await parser.get_day_info(selection, date)


@app.get('/api/schedule/{selection:path}/week/{week_num}')
async def send_schedule_week(selection: str, week_num: int):
    return await parser.get_week_info(selection.lower(), int(week_num))


@app.get('/api/schedule/{selection:path}/week/{week_num}/day/{day_num:int}/lesson/{lesson_id}')
async def send_lesson_by_week(selection: str, week_num: int, day_num: int, lesson_id: int):
    dates = await parser.get_dates(selection, week_num)
    date = dates[day_num - 1]
    return await parser.get_lesson_info(selection, date, lesson_id)


@app.get('/api/schedule/{selection:path}')
async def send_schedule(selection: str):
    return await parser.get_week_info(selection)
