#from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, Path, File, UploadFile,  Form
from typing import List, Optional
from uuid import UUID
import json

from app.core.models.usage_log import UsageLog
from app.core import constants


from app.schemas.usage_logs import (
    ListUsageLogResponse,
)

logs_router = APIRouter()


@logs_router.get("/", response_model=ListUsageLogResponse, tags=[constants.API_TAGS.LOGS])
async def list_logs(
) -> ListUsageLogResponse:
    logs = await UsageLog.find({}).sort('-timestamp').limit(10).to_list()

    return ListUsageLogResponse(logs=logs)
    