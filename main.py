from fastapi import FastAPI
from db import connect, disconnect

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await connect()


@app.on_event("shutdown")
async def shutdown_event():
    await disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}
