FROM python:3-alpine

RUN mkdir /app
WORKDIR /app
RUN apk update
RUN pip install --upgrade pip
ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app
EXPOSE 5000
ENTRYPOINT ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "5000", "--reload", "--log-config", "log.conf","app:app"]
