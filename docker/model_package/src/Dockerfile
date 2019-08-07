FROM docker.shehanigans.net/foundations-scheduler-worker-scheduler

RUN mkdir -p /job
RUN pip install flask-restful flask-cors

COPY ./model_package /job/model_package

WORKDIR /job

ENTRYPOINT ["python", "-m"]
CMD ["model_package"]
