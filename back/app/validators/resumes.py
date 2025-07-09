from __future__ import annotations

from typing import TYPE_CHECKING
from fastapi import HTTPException

from app.core.exceptions import InvalidObjectException
from app.core.models.resumes import Resume


async def validate_resume(resume: Resume) -> None:
    return 1
