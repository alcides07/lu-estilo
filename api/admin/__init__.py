from .product import ProductAdmin
from .category import CategoryAdmin
from .client import ClientAdmin
from .user import UserAdmin
from .order import OrderAdmin
from .order_product import OrderProductAdmin
from .administrator import AdministratorAdmin

all_admins = [
    ProductAdmin,
    CategoryAdmin,
    ClientAdmin,
    UserAdmin,
    OrderAdmin,
    OrderProductAdmin,
    AdministratorAdmin,
]
