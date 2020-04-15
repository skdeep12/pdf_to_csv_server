FROM python:3.7.7-slim

WORKDIR /app
ENV PYTHONBUFFERED 1
RUN python3.7 -m pip install -U pip setuptools
COPY requirements.txt /tmp/requirements.txt
RUN python3.7 -m pip install -U --no-cache-dir -r /tmp/requirements.txt

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]