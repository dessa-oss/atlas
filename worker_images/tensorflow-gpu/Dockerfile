FROM tensorflow/tensorflow:1.13.2-gpu-py3-jupyter

LABEL maintainer="Eric Kin Ho Lee" \
      version="0.1"

COPY ./foundations_gpu_requirements.txt /tmp/foundations_gpu_requirements.txt
COPY ./run.sh /prejob/run.sh

RUN chmod +x /prejob/run.sh

RUN pip install --requirement /tmp/foundations_gpu_requirements.txt
RUN rm /tmp/foundations_gpu_requirements.txt

ENTRYPOINT ["/prejob/run.sh"]

