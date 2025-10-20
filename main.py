from fastapi import FastAPI
from controller.controllers import router
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from contextlib import asynccontextmanager


app = FastAPI(title="String Analyzer Service (In-Memory)", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the String Analyzer Service API"}


@asynccontextmanager
async def lifespan(app: FastAPI):
        print("➡️ Proceeding without rate limiting.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)