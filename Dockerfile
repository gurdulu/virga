FROM python:3.8-alpine

COPY requirements.txt setup.py README.rst /app/
COPY virga/ /app/virga/
COPY bin/ /app/bin/

RUN pip install -e /app/ \
  && chmod +x /app/bin/*
