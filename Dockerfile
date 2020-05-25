FROM python:3.8-alpine

ARG ACTION=assert
ENV VIRGA_ACTION=${ACTION}

COPY requirements.txt setup.py README.rst /app/
COPY virga/ /app/virga/
COPY bin/ /app/bin/

RUN pip install -e /app/ \
  && chmod +x /app/bin/*

WORKDIR /app/bin

ENTRYPOINT /usr/bin/env python3 virga-${VIRGA_ACTION}
