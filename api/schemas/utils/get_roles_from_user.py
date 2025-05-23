from typing import List
from api.models.user import User
from api.schemas.role import Role


def get_roles_from_user(user: User):
    roles: List[Role] = []
    if user.client:
        roles.append(Role.CLIENT)

    if user.administrator:
        roles.append(Role.ADMINISTRATOR)

    return roles
