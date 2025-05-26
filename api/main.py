from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import all_routers
from database.config import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    title="API Lu Estilo - Sistema Comercial",
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


for router in all_routers:
    app.include_router(router)
