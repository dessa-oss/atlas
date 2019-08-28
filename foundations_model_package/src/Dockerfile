FROM docker.shehanigans.net/foundations-scheduler-worker-scheduler-no-gpu

RUN mkdir -p /tmp
COPY ./tmp /tmp
RUN pip install --no-index --find-links=/tmp/pip_wheels dessa-foundations foundations-rest-api 
RUN pip install flask-restful flask-cors

RUN mkdir -p /job
COPY ./foundations_model_package /job/foundations_model_package
COPY ./run.sh /job

ENV PYTHONPATH /job