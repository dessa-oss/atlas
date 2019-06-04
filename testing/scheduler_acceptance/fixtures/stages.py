"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def add_two_numbers(num1, num2):
    return num1 + num2

def get_ram_in_gb_when_limit_set():
    with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as memory_limit_file:
        memory_limit = memory_limit_file.read()

    return bytes_to_gigabytes(int(memory_limit))

def get_ram_in_gb_when_limit_not_set():
    with open('/proc/meminfo', 'r') as proc_info_file:
        proc_info_contents = proc_info_file.readlines()

    memtotal_line = list(filter(lambda line: line.startswith('MemTotal'), proc_info_contents))[0]
    memory_in_kb = memtotal_line.split(' ')[-2]
    return kilobytes_to_gigabytes(int(memory_in_kb))

def get_number_of_gpus():
    try:
        from tensorflow.python.client import device_lib
    except ImportError as ex:
        if _exception_thrown_because_no_gpus(ex):
            return 0
        raise

    local_device_protos = device_lib.list_local_devices()
    return len([device for device in local_device_protos if device.device_type == 'GPU'])

def print_message(message):
    print(message)

def _exception_thrown_because_no_gpus(exception):
    return 'libcuda.so.1: cannot open shared object file: No such file or directory' in str(exception)

def bytes_to_gigabytes(number_in_bytes):
    return number_in_bytes / 1024 / 1024 / 1024

def kilobytes_to_gigabytes(number_in_kilobytes):
    return number_in_kilobytes / 1024 / 1024