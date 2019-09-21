FROM python:3.7-slim-buster

LABEL maintainer="areed145@gmail.com"

WORKDIR /aprs-entry

COPY . /aprs-entry

# We copy just the requirements.txt first to leverage Docker cache
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# EXPOSE 80

ENV NAME World

CMD ["python", "aprs-entry.py"]