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


@app.get('/api/schedule/{selection:path}/week/{week_num:int}')
async def send_schedule_week(selection: str, week_num: int):
    return await parser.get_week_info(selection, week_num)


@app.get('/api/schedule/{selection:path}')
async def send_schedule(selection: str):
    return await parser.get_week_info(selection)
