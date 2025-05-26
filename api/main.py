import sentry_sdk
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import all_routers
from database.config import Base, engine
from decouple import config

SENTRY_DSN = config("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


for router in all_routers:
    app.include_router(router)
