from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models
from .database import engine
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)

    yield

    engine.dispose()


app = FastAPI(
    title="Lost Media Archive API",
    lifespan=lifespan,
)

app.include_router(router)