from .client import router as client_router
from .administrator import router as administrator_router
from .auth import router as auth_router
from .product import router as product_router
from .category import router as category_router

all_routers = [
    client_router,
    administrator_router,
    auth_router,
    product_router,
    category_router,
]
