
FROM tensorflow/tensorflow:1.14.0-py3

# Where the tensorboard log dir mounts
VOLUME /logs
# Where the job archive mounts
VOLUME /archive
EXPOSE 6006
CMD tensorboard --logdir /logs
