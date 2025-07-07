from fastapi import FastAPI
from slack_handler import router

app = FastAPI()
app.include_router(router)
