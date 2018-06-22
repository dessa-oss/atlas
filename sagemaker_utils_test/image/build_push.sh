`aws ecr get-login --no-include-email --region us-east-1`
docker build -t sagemaker-foundations .
docker tag sagemaker-foundations:latest 725911994102.dkr.ecr.us-east-1.amazonaws.com/sagemaker-foundations:latest
docker push 725911994102.dkr.ecr.us-east-1.amazonaws.com/sagemaker-foundations:latest