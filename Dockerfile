FROM python:3.9

RUN mkdir -p /usr/src/fastapi-post-crud

COPY requirements.txt /usr/src/fastapi-post-crud/

WORKDIR /usr/src/fastapi-post-crud

RUN pip install -r requirements.txt