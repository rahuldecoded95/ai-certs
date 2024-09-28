FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3.10 python3-pip



RUN pip3 install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache -r /app/requirements.txt

WORKDIR /app

COPY . /app