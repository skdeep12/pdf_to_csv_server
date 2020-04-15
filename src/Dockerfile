FROM revolutionsystems/python:3.7.1-wee-optimized-lto

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y g++
RUN apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
COPY ./src /app
WORKDIR /app

ENV PYTHONBUFFERED 1
RUN python3.7 -m pip install -U pip setuptools
COPY requirements.txt /tmp/requirements.txt
RUN python3.7 -m pip install -U --no-cache-dir -r /tmp/requirements.txt

RUN cp /app/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]