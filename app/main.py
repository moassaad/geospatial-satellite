from pydantic import BaseModel
from fastapi import FastAPI


class RootResponse(BaseModel):
    message: str


app = FastAPI(title="Geospatial Satellite Data API")


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message="Hello World")
