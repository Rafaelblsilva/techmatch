from typing import Optional, Union
from uuid import UUID
from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.core.models.metadata import Metadata, metadata_field



class UsageLog(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    request_id : UUID
    user_id : str
    timestamp :  datetime = Field(default_factory=datetime.utcnow)
    query : Optional[str]
    resultado : str
    metadata: Metadata = metadata_field


    class Settings:
        name = "usage_logs"
