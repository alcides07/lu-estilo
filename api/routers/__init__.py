from routers.client import router as client_router
from routers.administrator import router as administrator_router
from routers.auth import router as auth_router
from routers.product import router as product_router
from routers.category import router as category_router

all_routers = [
    client_router,
    administrator_router,
    auth_router,
    product_router,
    category_router,
]
