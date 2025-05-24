from typing import List
from models.user import User
from schemas.role import Role


def get_roles_from_user(user: User):
    roles: List[Role] = []
    if user.client:
        roles.append(Role.CLIENT)

    if user.administrator:
        roles.append(Role.ADMINISTRATOR)

    return roles
