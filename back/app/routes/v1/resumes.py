#from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, Path, File, UploadFile,  Form
from typing import List, Optional
from uuid import UUID
from fastapi.responses import JSONResponse
import json

from app.core.database import get_db
from app.core.exceptions import InvalidObjectException
from app.core.models.user import User
from app.core.models.resumes import Resume
from app.core.models.usage_log import UsageLog

from app.schemas.resumes import (
    PostResumeResponse,
    ProcessResumesRequest
)
from hashlib import sha256
from app.resume_processor import extract_resume_text
from app.resume_summarizer import summarize_resume, query_on_resume, rate_query_on_resume
from app.core import constants

#from app.middlewares.auth_middleware import UserDep
from app.validators.resumes import validate_resume

resumes_router = APIRouter()


@resumes_router.post("/", response_model=PostResumeResponse, tags=[constants.API_TAGS.RESUMES])
async def create_resume(
#    current_user: UserDep,
    file: UploadFile = File(...)
) -> PostResumeResponse:
    
    content = await file.read(-1)
    content_type = file.content_type
    file_hash = sha256(content).hexdigest()


    # Check resume metadata
    existing_resume = await Resume.find({"raw_hash": file_hash, "raw_size": file.size}).to_list()
    if len(existing_resume) > 0:
        raise HTTPException(
            status_code=400, detail="We have your resume already, Thanks for you application!"
        )
    
    text = extract_resume_text(content, ext=content_type)
    summary = summarize_resume(text)
    new_resume = Resume(
        size_bytes=file.size,
        sha256=file_hash,
        summary=summary
    )
    #new_resume.metadata.set_create(user_id=current_user.id)
    new_resume.metadata.set_create()
    await validate_resume(new_resume)
    
    # create document in resumes collection
    await new_resume.insert()

    return PostResumeResponse(**new_resume.dict())



@resumes_router.post("/process-resumes/", tags=[constants.API_TAGS.RESUMES])
async def process_resumes(
    body: ProcessResumesRequest  = Body(..., openapi_examples=ProcessResumesRequest.Config.examples),
):
    results = []

    for file in body.files:
        text = extract_resume_text(file.content_base64)
        if body.query:
            summary = summarize_resume(text)
            query_result = query_on_resume(text, body.query)
            query_score = rate_query_on_resume(text, body.query, query_result)
            results.append({
                "filename": file.filename,
                "summary": summary,
                "query_result": query_result,
                "query_score": query_score
            })
        else:
            summary = summarize_resume(text)
            results.append({
                "filename": file.filename,
                "summary": summary
            })

    usage_log = UsageLog(
        request_id = body.request_id,
        user_id = body.user_id,
        query = body.query,
        resultado = json.dumps(results)
    )
    await usage_log.insert()


    return JSONResponse(content={
        "request_id": str(body.request_id),
        "user_id": body.user_id,
        "results": results
    })