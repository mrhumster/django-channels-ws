FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /app/
WORKDIR /app/
RUN ls -lh /app/
RUN apk add gcc musl-dev libffi-dev
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir  -r requirements.txt
COPY wschat /app/