from pydantic import BaseModel
from app.core.models.usage_log import UsageLog

class ListUsageLogResponse(BaseModel):
    logs: list['UsageLog']

