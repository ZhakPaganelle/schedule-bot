"""Parsed API from rasp.rea.ru"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello/", response_model=str)
async def hello():
    """Test function"""
    return "Hello"
