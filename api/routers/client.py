from fastapi import APIRouter
from api.dependencies.get_session_db import SessionDep
from api.orm.client import create_client
from api.schemas.client import ClientCreate, ClientRead


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    # dependencies=[Depends(get_authenticated_user)],
)


@router.post("/", response_model=ClientRead, status_code=201)
async def create(client: ClientCreate, session: SessionDep):
    data = create_client(client, session)
    return data
