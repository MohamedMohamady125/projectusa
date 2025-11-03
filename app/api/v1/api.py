"""
Main API router that combines all endpoint routers.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    athletes,
    schools,
    tasks,
    recruitment,
    documents,
    communications,
    tutorials,
    notifications,
    stats,
    admin
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(athletes.router, prefix="/athletes", tags=["Athletes"])
api_router.include_router(schools.router, prefix="/schools", tags=["Schools"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(recruitment.router, prefix="/recruitment", tags=["Recruitment"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(communications.router, prefix="/communications", tags=["Communications"])
api_router.include_router(tutorials.router, prefix="/tutorials", tags=["Tutorials"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(stats.router, prefix="/stats", tags=["Statistics"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
