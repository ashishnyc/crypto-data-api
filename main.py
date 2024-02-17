from fastapi import FastAPI
from db.db_setup import get_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
