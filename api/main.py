import sentry_sdk
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqladmin import Admin
from routers import all_routers
from database.config import Base, engine
from decouple import config
from admin import all_admins

SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN is not None:
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


app = FastAPI(
    lifespan=lifespan,
    title="👨👔👘👩‍🦰 API Lu Estilo - Sistema Comercial",
    docs_url=None,
    redoc_url=None,
    description="""## 📌 Visão Geral    
    A API Lu Estilo é a solução tecnológica desenvolvida para potencializar as operações comerciais 
    da Lu Estilo, empresa de confecção que busca expandir seus canais de vendas.
    ### 🚀 Solução Proposta
    Esta API RESTful fornece:
    - Gestão de clientes
    - Controle de estoque de produtos
    - Gerenciamento de pedidos
    """,
)

admin = Admin(app, engine)
for adm in all_admins:
    admin.add_view(adm)

for router in all_routers:
    app.include_router(router)
