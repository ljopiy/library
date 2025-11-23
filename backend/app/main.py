from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.routes import api_router
from db.base import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app...")
    await create_tables()
    yield
    print("Stopping app...")


app = FastAPI(
    title="Library Management System",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в Library Management System!",
        "description": "API для управления библиотекарями, пользователями, книгами, жанрами и сериями.",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "status": "OK",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
