from .admin import router as admin_router
from .menu import router as menu_router
from .poll import router as poll_router
from .registration import router as registration_router

__all__ = ("registration_router", "admin_router", "poll_router", "menu_router")
