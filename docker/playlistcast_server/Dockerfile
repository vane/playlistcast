FROM python:3.7.6-alpine3.11
MAINTAINER michal@vane.pl
RUN apk add --no-cache git build-base
ADD . /install
RUN git clone https://github.com/vane/tornadoql /vendor/tornadoql
RUN pip install -r /install/requirements.py37.txt
