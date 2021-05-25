FROM python:3.9.5-buster AS builder

ADD ./setup /usr/local/setup
RUN pip install -r /usr/local/setup/requirements.txt

ADD ./app /usr/local/app

ENTRYPOINT ["flask", "run"]

WORKDIR /usr/local/app/
