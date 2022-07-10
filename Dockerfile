FROM python:3.9-alpine

LABEL maintainer="narendhar15@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
# Flush the buffer
ENV PYTHONUNBUFFERED=1

# Compilation dependencies 
# TODO : Check if all dependencies is needed
RUN apk update && apk add bash gcc jpeg-dev musl-dev procps \
    libffi-dev openssl-dev zlib-dev gettext

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt