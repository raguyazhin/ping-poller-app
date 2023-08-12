FROM python:3.8-slim-buster

WORKDIR /app

COPY ping-poller.py /app/
COPY requirements.txt /app/

RUN apt-get update && \
    apt-get install -y iputils-ping && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "ping-poller.py"]
