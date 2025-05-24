from ..database.config import Session
from typing import Annotated
from fastapi import Depends


def get_session_db():
    db = Session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session_db)]
