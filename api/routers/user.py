from fastapi import APIRouter
from api.dependencies.get_session_db import SessionDep
from api.orm.user import create_user
from api.schemas.user import UserCreate, UserRead


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_authenticated_user)],
)


@router.post("/", response_model=UserRead, status_code=201)
async def create(user: UserCreate, session: SessionDep):
    data = create_user(user, session)
    return data
