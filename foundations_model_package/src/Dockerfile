FROM docker.shehanigans.net/foundations-scheduler-worker-scheduler

RUN mkdir -p /job
RUN pip install flask-restful flask-cors

COPY ./foundations_model_package /job/foundations_model_package

WORKDIR /job

ENTRYPOINT ["python", "-m"]
CMD ["foundations_model_package"]
