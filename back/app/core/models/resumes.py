from typing import Optional, Union
from uuid import UUID

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.core.models.metadata import Metadata, metadata_field



class Resume(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    version: int = Field(default=1)
    # Save a checksum of file to see if they are submitted again
    size_bytes: int
    sha256: str
    summary: str
    metadata: Metadata = metadata_field

    class Settings:
        name = "resume"