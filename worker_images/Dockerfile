FROM python:3.7-alpine

LABEL maintainer="Eric Kin Ho Lee"

RUN apk --update add --no-cache g++ make

COPY ./foundations_requirements.txt /tmp/foundations_requirements.txt
COPY ./run.sh /prejob/run.sh

RUN chmod +x /prejob/run.sh

RUN pip install --requirement /tmp/foundations_requirements.txt
RUN rm /tmp/foundations_requirements.txt

ENTRYPOINT ["/prejob/run.sh"]
