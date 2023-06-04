FROM python:3.10-alpine

COPY requirements.txt /
RUN apk add build-base
RUN pip install -r requirements.txt

COPY bot /app/bot

WORKDIR /app
CMD python -m bot