from .admin import router as admin_router
from .poll import (
    exam_router,
    task1_router,
    task2_router,
    task3_router,
    task4_router,
    task5_router,
    task6_router,
    task7_router,
    task8_router,
    task9_router,
    task10_router,
    task11_router,
    task12_router,
    task13_router,
)
from .poll import router as poll_router
from .registration import router as registration_router

__all__ = (
    "registration_router",
    "admin_router",
    "poll_router",
    "task1_router",
    "task2_router",
    "task3_router",
    "task4_router",
    "task5_router",
    "task6_router",
    "task7_router",
    "task8_router",
    "task9_router",
    "task10_router",
    "task11_router",
    "task12_router",
    "task13_router",
    "exam_router",
)
