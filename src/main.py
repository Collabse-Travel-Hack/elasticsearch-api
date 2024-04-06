from fastapi import FastAPI
from src.api.endpoints import get_record, get_index

app = FastAPI()

app.include_router(get_record)
app.include_router(get_index)
