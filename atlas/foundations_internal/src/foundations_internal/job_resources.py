

class JobResources(object):
    def __init__(self, num_gpus, ram):
        self.num_gpus = num_gpus
        self.ram = ram

    def __eq__(self, other_job_resources):
        return self.num_gpus == other_job_resources.num_gpus and self.ram == other_job_resources.ram