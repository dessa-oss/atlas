
import foundations

parameters = foundations.load_parameters(log_parameters=False)
job_id = parameters['source_job_id']

first_directory = foundations.create_syncable_directory('some data', 'results', source_job_id=job_id)
first_directory.upload()

second_directory = foundations.create_syncable_directory('some metadata', 'metadata', source_job_id=job_id)
second_directory.upload()