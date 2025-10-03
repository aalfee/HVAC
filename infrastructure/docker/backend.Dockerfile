# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ../../backend /app
COPY ../../requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
