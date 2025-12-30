"""API routes module."""

from src.routes.auth import router as auth_router
from src.routes.tasks import router as tasks_router
from src.routes.tags import router as tags_router

__all__ = ["auth_router", "tasks_router", "tags_router"]
