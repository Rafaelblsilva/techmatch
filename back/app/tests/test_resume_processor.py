import pytest
from app.resume_processor import *



@pytest.mark.parametrize("filepath", [
    "/app/tests/fixtures/resumes/sample_resume.pdf",
    "/app/tests/fixtures/resumes/sample_resume.png",
    "/app/tests/fixtures/resumes/sample_resume.jpg",
    "/app/tests/fixtures/resumes/sample_resume.jpeg",
    "/app/tests/fixtures/resumes/sample_resume.tiff",
    "/app/tests/fixtures/resumes/sample_resume.bmp",
])
def test_extractions(filepath):
    result = extract_resume_text(filepath)
    print(f"Extracted from {filepath}: {result}")
    assert result is not None and result != "", f"Extraction failed for {filepath}"