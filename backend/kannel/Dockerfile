FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y build-essential wget libxml2-dev libmysqlclient-dev libssl-dev curl

RUN apt-get install kannel -y 

COPY kannel.conf /etc/kannel/kannel.conf

