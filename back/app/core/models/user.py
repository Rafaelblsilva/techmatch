from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    updated_at: datetime = datetime.utcnow()
