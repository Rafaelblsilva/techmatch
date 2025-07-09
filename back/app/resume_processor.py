from io import BytesIO
import base64
import magic
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
import fitz  # PyMuPDF

from app.core.exceptions import InvalidObjectException
from app.core.config import setup_logger
from app.schemas.resumes import ResumeFile
logger = setup_logger('resume_processor')


def detect_mime_type(file_bytes):
    mime = magic.Magic(mime=True)
    return mime.from_buffer(file_bytes)

def detect_extension(file_bytes):
    mime_type = detect_mime_type(file_bytes)
    mapping = {
        "application/pdf": ".pdf",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/tiff": ".tiff",
        "image/bmp": ".bmp",
    }
    return mapping.get(mime_type, None)

def extract_text_from_pdf(file):
    """Try normal PDF text extraction first"""
    try:
        text = ""
        if isinstance(file, bytes):
            file = BytesIO(file)
            doc = fitz.open(stream=file, filetype="pdf")
        else:
            doc = fitz.open(file)  # Assume it's a path

        with doc:
            for page in doc:
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
        if text.strip():
            return text
    except Exception as e:
        logger.error(f"Error reading normal PDF: {e}")
    return None

def extract_text_from_scanned_pdf(file):
    """Fallback OCR for scanned PDFs"""
    text = ""
    try:
        if isinstance(file, bytes):
            file = BytesIO(file)
            images = convert_from_bytes(file.read())
        elif isinstance(file, str):
            images = convert_from_path(file)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
    except Exception as e:
        logger.error(f"Error performing OCR on PDF: {e}")
    return text


def extract_text_from_image(file):
    try:
        if isinstance(file, bytes):
            file = BytesIO(file)
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    except Exception as e:
        logger.error(f"Error reading image: {e}")
    return ""


def process_resume_text(file, ext):
    if ext == ".pdf":
        text = extract_text_from_pdf(file)
        if not text.strip():
            logger.error(f"Fallback to OCR for scanned PDF...")
            text = extract_text_from_scanned_pdf(file)
        return text
    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
        return extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file type.")

def extract_resume_text(file, ext=None):
    # Check if its present in filesystem
    if os.path.exists(file):
        ext = os.path.splitext(file)[1].lower()
        return process_resume_text(file, ext)
    
    try:
        if not ext:
            ext = detect_extension(file)
        else:
            ext = {
                "application/pdf": ".pdf",
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "image/tiff": ".tiff",
                "image/bmp": ".bmp",
            }.get(ext, ext)

        print('RAW_FILE_END')
        return process_resume_text(file, ext)

    except:
        pass
    # Assume its b64 encoded
    try:
        raw_file = base64.b64decode(file)
    except:
        rf = ResumeFile(
            filename = '-',
            content_type = '-',
            content_base64 = str(file)
        )
        raise InvalidObjectException(rf, 'Unsupported file type.')
    ext = detect_extension(raw_file)
    if not ext:
        rf = ResumeFile(
            filename = '-',
            content_type = '-',
            content_base64 = str(file)
        )
        raise InvalidObjectException(rf, 'Unsupported file type.')
    return process_resume_text(raw_file, ext)


if __name__ == "__main__":
    pass
