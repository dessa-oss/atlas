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