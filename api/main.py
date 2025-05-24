from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import all_routers
from database.config import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


for router in all_routers:
    app.include_router(router)
