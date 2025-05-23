from .client import router as client_router
from .administrator import router as administrator_router
from .auth import router as auth_router

all_routers = [client_router, administrator_router, auth_router]
