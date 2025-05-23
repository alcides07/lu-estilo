from enum import Enum


class Role(str, Enum):
    ADMINISTRATOR = "administrator"
    CLIENT = "client"
