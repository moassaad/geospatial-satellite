from pydantic import BaseModel
from fastapi import FastAPI

from app.config.settings import Settings

settings = Settings()


class RootResponse(BaseModel):
    message: str


app = FastAPI(title=settings.app_name)


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message="Hello World")
