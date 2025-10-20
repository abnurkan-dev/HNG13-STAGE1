from fastapi import FastAPI
from controller.controllers import router

app = FastAPI(title="String Analyzer Service (In-Memory)", version="1.0.0")
app.include_router(router)
