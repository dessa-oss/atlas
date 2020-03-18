
FROM python:3.6.8-alpine as base

# Install requirements in a separate container
FROM base as builder
RUN mkdir /install
WORKDIR /install
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --prefix=/install -r requirements.txt

FROM base
COPY --from=builder /install /usr/local
RUN mkdir /app
WORKDIR /app
ADD . /app/

# Where the tensorboard logdir mounts
VOLUME /logs
# Where the job archive mounts
VOLUME /archive

EXPOSE 5000

CMD ["python", "/app/tensorboard_rest_api_server.py"]