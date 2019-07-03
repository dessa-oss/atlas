"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations

def get_ram_in_gb_when_limit_not_set():
    with open('/proc/meminfo', 'r') as proc_info_file:
        proc_info_contents = proc_info_file.readlines()

    memtotal_line = list(filter(lambda line: line.startswith('MemTotal'), proc_info_contents))[0]
    memory_in_kb = memtotal_line.split(' ')[-2]
    return kilobytes_to_gigabytes(int(memory_in_kb))

def get_number_of_gpus():
    from tensorflow.python.client import device_lib

    local_device_protos = device_lib.list_local_devices()
    return len([device for device in local_device_protos if device.device_type == 'GPU'])

def bytes_to_gigabytes(number_in_bytes):
    return number_in_bytes / 1024 / 1024 / 1024

def kilobytes_to_gigabytes(number_in_kilobytes):
    return number_in_kilobytes / 1024 / 1024

foundations.log_metric('memory', get_ram_in_gb_when_limit_not_set())
foundations.log_metric('gpus', get_number_of_gpus())