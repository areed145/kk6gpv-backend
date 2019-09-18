FROM python:3.7-slim-buster

LABEL maintainer="areed145@gmail.com"

WORKDIR /wunderground

COPY . /wunderground

# We copy just the requirements.txt first to leverage Docker cache
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# EXPOSE 80

ENV NAME World

CMD ["python", "wunderground.py"]