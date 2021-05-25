FROM python:3.9.5-buster AS builder

ADD ./app /usr/local/app

ENTRYPOINT ["flask", "run"]
