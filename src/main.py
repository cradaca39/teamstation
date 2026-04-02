from fastapi import FastAPI

from src.api import router

app = FastAPI(title="Items API", version="1.0.0")
app.include_router(router)
