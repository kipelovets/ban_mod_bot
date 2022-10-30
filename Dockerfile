FROM python:3.10

COPY docker/app/requirements.txt /
RUN pip install -r requirements.txt

COPY bot /app/bot

WORKDIR /app
CMD python -m bot