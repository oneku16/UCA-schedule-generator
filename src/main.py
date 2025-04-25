from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import user
from src.api.routers import schedule
from src.infrastructure.database import create_db_and_tables


@asynccontextmanager
async def startup(app_: FastAPI):
    yield await create_db_and_tables()


app = FastAPI(
    title="Bookaroom Admin panel",
    description="API for creating and updating schedule for UCA.",
    version="1.0",
    contact={
        "name": "Elnazar Ulanbek uulu",
        "email": "elnazar.ulanbekuulu@outlook.com",
    },
    license_info={"name": "MIT License"},
    lifespan=startup
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/auth", tags=["Users"])
app.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])


@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Welcome!"}
