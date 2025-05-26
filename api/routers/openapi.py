from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import APIRouter

router = APIRouter()


@router.get("/docs/", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Lu Estilo",
        swagger_favicon_url="https://cdn3.iconfinder.com/data/icons/fashion-flat-icons-vol-1/256/02-512.png",
        swagger_ui_parameters={
            "syntaxHighlight": {"theme": "nord"},
            "filter": True,
            "deepLinking": True,
            "displayRequestDuration": True,
            "tryItOutEnabled": True,
        },
    )


@router.get("/redoc/", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="API Lu Estilo",
        redoc_favicon_url="https://cdn3.iconfinder.com/data/icons/fashion-flat-icons-vol-1/256/02-512.png",
    )
