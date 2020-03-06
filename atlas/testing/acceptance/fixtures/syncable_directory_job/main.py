
import foundations

first_directory = foundations.create_syncable_directory('some data', 'results')
first_directory.upload()

second_directory = foundations.create_syncable_directory('some metadata', 'metadata')
second_directory.upload()