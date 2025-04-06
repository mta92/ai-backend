FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx && \
    pip install --upgrade pip

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]