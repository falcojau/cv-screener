from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI()

@app.get("/")
async def inicio():
    return {"mensaje": "Mi segunda API con FastAPI funciona 😍"}