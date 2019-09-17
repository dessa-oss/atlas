FROM docker.shehanigans.net/foundations-scheduler-worker-scheduler-no-gpu

RUN mkdir -p /tmp
COPY ./tmp /tmp
RUN pip install --no-index --find-links=/tmp/pip_wheels dessa-foundations foundations-rest-api 
RUN pip install flask-restful flask-cors
RUN apt-get update && apt-get install -y gettext-base netcat && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.10.3/bin/linux/amd64/kubectl > kubectl && \
        chmod +x ./kubectl && \
        mv ./kubectl /usr/local/bin/kubectl

RUN mkdir -p /job
COPY ./foundations_model_package /job/foundations_model_package
COPY ./run.sh /job

ENV PYTHONPATH /job