from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/hello/', response_model=str)
async def hello():
    return 'Hello'
