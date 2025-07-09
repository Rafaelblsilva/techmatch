from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from pathlib import Path


current_file = Path(__file__).resolve()
app_dir = current_file.parent.parent
resume_fixtures =  str(app_dir.absolute() / 'tests' / 'fixtures' / 'resumes')
import base64

pdf_resume = base64.b64encode(open(resume_fixtures + '/sample_resume.pdf', 'rb').read())
jpg_resume = base64.b64encode(open(resume_fixtures + '/sample_resume.jpg', 'rb').read())

from app.core.models.resumes import Resume
#from app.validators.resume import validate_resume


class ResumeFile(BaseModel):
    filename: str
    content_type: Optional[str]
    content_base64: str  # base64-encoded file content

#region requests 

class ProcessResumesRequest(BaseModel):
    files: List[ResumeFile]
    query: Optional[str] = None
    request_id: Optional[UUID] = None
    user_id: Optional[str] = None

    class Config:
        examples = {
            "standard": {
                "summary": "Request Padrão",
                "description": 'Contém query para processamento dos currículos que mais se enquadram, acompanhados de uma justificativa e um resumo de cada um dos currículos.',
                "value": {
                "files": [
                    {
                    "filename": "resume1.pdf",
                    "content_type": "application/pdf",
                    "content_base64": pdf_resume
                    },
                    {
                    "filename": "resume2.jpg",
                    "content_type": "image/jpg",
                    "content_base64": jpg_resume
                    }
                ],
                "query": "Qual desses currículos se enquadra melhor para a vaga de Engenheiro de Software com esses requisitos: Python, React, AWS, GCP, Terraform",
                "request_id": "7a9c6464-3e61-4a91-bfa4-0f9b4e3df7b9",
                "user_id": "fabio.techmatch"
                },
            },
            "queryless": {
                "summary": "Sumários individuais",
                "description": 'Caso query não seja informada, é retornado um resumo individual dos currículos',
                "value": {
                "files": [
                    {
                    "filename": "resume1.pdf",
                    "content_type": "application/pdf",
                    "content_base64": pdf_resume
                    },
                    {
                    "filename": "resume2.jpg",
                    "content_type": "image/jpg",
                    "content_base64": jpg_resume
                    }
                ],
                "request_id": "8a9c6464-3e61-4a91-bfa4-0f9b4e3df7b9",
                "user_id": "fabio.techmatch"
                },
            },
            "error_invalid_request":  {
                "summary": "Request inválido",
                "description": 'Erro arquivo inválido',
                "value": {
                "files": [
                    {
                    "filename": "resume1.pdf",
                    "content_type": "application/pdf",
                    "content_base64": '123'
                    },
                ],
                "request_id": "9a9c6464-3e61-4a91-bfa4-0f9b4e3df7b9",
                "user_id": "fabio.techmatch"
                },
            },
        }

#endregion requests


#region responses
class PostResumeResponse(BaseModel):
    size_bytes: int
    sha256: str
    summary: str

#endregion responses
