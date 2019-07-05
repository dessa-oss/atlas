FROM docker.shehanigans.net/foundations-scheduler-worker-scheduler

RUN mkdir -p /job
RUN pip install flask-restful

COPY run.sh /job
COPY api.py /job
