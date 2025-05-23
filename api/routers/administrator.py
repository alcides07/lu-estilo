from fastapi import APIRouter
from api.dependencies.get_session_db import SessionDep
from api.orm.administrator import create_administrator
from api.schemas.administrator import AdministratorCreate, AdministratorRead


router = APIRouter(
    prefix="/administrators",
    tags=["administrators"],
    # dependencies=[Depends(get_authenticated_user)],
)


@router.post("/", response_model=AdministratorRead, status_code=201)
async def create(administrator: AdministratorCreate, session: SessionDep):
    data = create_administrator(administrator, session)
    return data
