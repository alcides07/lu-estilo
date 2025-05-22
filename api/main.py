from fastapi import FastAPI
from api.routers import all_routers
from contextlib import asynccontextmanager
from api.database.config import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


for router in all_routers:
    app.include_router(router)
