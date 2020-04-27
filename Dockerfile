FROM python:3.8-slim
MAINTAINER https://github.com/rsbyrne/

WORKDIR /

ADD . /fbapi

RUN apt-get update -y
RUN apt-get install -y apt-utils
RUN apt-get install -y tar
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y unzip
RUN apt-get install -y firefox-esr

WORKDIR /usr/bin

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN rm geckodriver*.tar.gz
RUN chmod +x geckodriver

WORKDIR /

RUN pip install --no-cache-dir selenium
