from .user import router as user_router
from .client import router as client_router
from .administrator import router as administrator_router

all_routers = [user_router, client_router, administrator_router]
