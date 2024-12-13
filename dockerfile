FROM python:3-alpine

ENV TZ="Europe/Amsterdam"

COPY sp/* /sp/
WORKDIR /sp

ENTRYPOINT ["python3", "main.py"]
