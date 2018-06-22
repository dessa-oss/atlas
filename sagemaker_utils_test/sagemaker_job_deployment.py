import sagemaker as sage
from s3_bucket import S3Bucket

from os import chdir, getcwd
from glob import glob
import tarfile
import uuid

role = "AmazonSageMaker-ExecutionRole-20180620T133208" # need to specify
image = "725911994102.dkr.ecr.us-east-1.amazonaws.com/sagemaker-foundations:latest" # need to specify
job_name = str(uuid.uuid4()) # can come from internal job name
bucket_name = "sagemaker-us-east-1-725911994102" # need to specify - maybe can come from pipeline archive?
instance_type = "ml.c4.2xlarge" # need to specify
number_of_instances = 1 # until we figure out distributed training, leave this at 1

session = sage.Session()
bucket = S3Bucket(bucket_name)
job_archive_name = job_name + ".tgz"

cwd = getcwd()

with tarfile.open(job_archive_name, "w:gz") as tar:
    chdir("test_job")
    for path in glob("*"):
        tar.add(path)

    chdir(cwd)

bucket.upload_from_file(job_archive_name, job_archive_name)

tree = sage.estimator.Estimator(image, role, number_of_instances, instance_type, sagemaker_session=session)
# job name must satisfy ^[a-zA-Z0-9](-*[a-zA-Z0-9])*
# (must start with alphanumeric character, and then dashes + alphanumeric)
tree.fit(bucket.s3_address(job_archive_name), wait=False, logs=False, job_name=job_name)