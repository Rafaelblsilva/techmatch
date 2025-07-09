from fastapi import APIRouter

from app.routes.v1.resumes import resumes_router
from app.routes.v1.usage_logs import logs_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(resumes_router, prefix="/resumes")
api_router.include_router(logs_router, prefix="/logs")


