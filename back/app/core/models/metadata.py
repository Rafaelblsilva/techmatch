from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.constants import DEFAULT_SYSTEM_UUID


class Metadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: UUID = Field(default=DEFAULT_SYSTEM_UUID)
    updated_by: UUID = Field(default=DEFAULT_SYSTEM_UUID)

    def set_update(self, user_id=None):
        self.updated_at = datetime.utcnow()
        if user_id:
            self.updated_by = user_id

    def set_create(self, user_id=None):
        self.updated_at = datetime.utcnow()
        self.created_at = datetime.utcnow()
        if user_id:
            self.updated_by = user_id
            self.created_by = user_id


metadata_field = Field(default=Metadata())
