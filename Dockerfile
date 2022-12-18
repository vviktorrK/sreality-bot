# syntax=docker/dockerfile:1

FROM ubuntu:20.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-pip

WORKDIR /sreality-bot

RUN apt-get -y install libpq-dev
RUN pip3 install psycopg2 Flask Scrapy scrapy-playwright

ENV DEBIAN_FRONTEND noninteractive
RUN playwright install --with-deps chromium

COPY . .
RUN chmod u+x bin/wait-for-it.sh
RUN chmod u+x bin/run.sh

CMD ["./bin/wait-for-it.sh", "postgres_db:5432", "--", "./bin/run.sh"]