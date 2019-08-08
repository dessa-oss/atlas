FROM python:3.6.8-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --install-option="--prefix=/install" -r requirements.txt

FROM base

COPY --from=builder /install /usr/local

RUN mkdir /app
WORKDIR /app
ADD . /app/

EXPOSE 5000
CMD ["python", "/app/test_server.py"]