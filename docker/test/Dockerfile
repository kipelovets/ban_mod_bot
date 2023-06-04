FROM python:3.10-alpine

COPY requirements.txt /

RUN apk add build-base
RUN pip install -r requirements.txt
RUN pip install coverage pytest-asyncio pyairtable pylint autopep8
RUN apk add npm && npm install -g pyright
RUN mkdir /app && chown -R root /app

VOLUME [ "/app" ]