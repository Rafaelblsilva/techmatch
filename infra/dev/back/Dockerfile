FROM python:3.12

RUN pip install --upgrade pip

RUN apt update

RUN apt install tesseract-ocr -y

RUN adduser --system --no-create-home nonroot

COPY back/app/ /app

WORKDIR /

RUN pip install -r app/requirements.txt


HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -f http://localhost:8080 || exit 1

USER nonroot
CMD ["uvicorn", "app.main:app" , "--host", "0.0.0.0", "--port", "8080"]

