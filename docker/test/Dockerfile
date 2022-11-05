FROM python:3.10

COPY requirements.txt /

RUN pip install -r requirements.txt
RUN pip install coverage pytest-asyncio pyairtable pylint autopep8
RUN apt-get update && apt-get install -y npm && npm install -g pyright
RUN mkdir /app && chown -R root /app

VOLUME [ "/app" ]