"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations

def get_ram_in_gb_when_limit_set():
    with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as memory_limit_file:
        memory_limit = memory_limit_file.read()

    return bytes_to_gigabytes(int(memory_limit))

def get_number_of_gpus():
    from tensorflow.python.client import device_lib

    local_device_protos = device_lib.list_local_devices()
    return len([device for device in local_device_protos if device.device_type == 'GPU'])

def bytes_to_gigabytes(number_in_bytes):
    return number_in_bytes / 1024 / 1024 / 1024

def kilobytes_to_gigabytes(number_in_kilobytes):
    return number_in_kilobytes / 1024 / 1024

foundations.log_metric('memory', get_ram_in_gb_when_limit_set())
foundations.log_metric('gpus', get_number_of_gpus())