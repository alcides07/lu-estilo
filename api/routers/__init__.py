from routers.client import router as client_router
from routers.administrator import router as administrator_router
from routers.auth import router as auth_router
from routers.product import router as product_router
from routers.category import router as category_router
from routers.order import router as order_router
from routers.openapi import router as openapi_router

all_routers = [
    administrator_router,
    auth_router,
    category_router,
    client_router,
    product_router,
    order_router,
    openapi_router,
]
