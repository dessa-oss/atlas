# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 11 2018

FROM tensorflow/tensorflow:latest-py3

# Where the tensorboard log dir mounts
VOLUME /logs
# Where the job archive mounts
VOLUME /archive
EXPOSE 6006
CMD tensorboard --logdir /logs
