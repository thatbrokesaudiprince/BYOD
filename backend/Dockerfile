# fastapi_app/Dockerfile
FROM python:3.11-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/backend
#uncomment for production
WORKDIR /app/backend


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
