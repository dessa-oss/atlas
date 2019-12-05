#!/bin/bash

instance_name=$(head /dev/urandom | LC_CTYPE=C tr -dc A-Za-z0-9 | head -c 13 ; echo '')
echo "export instance_name=$instance_name" > k8s_instance_name.sh

export ANSIBLE_HOST_KEY_CHECKING=False

echo Creating instance $instance_name

ansible-playbook -e instance_name=$instance_name deploy_docker_local_scheduler_instance.yaml && \
    ansible-playbook --private-key ~/.ssh/jenkins.pem -i ec2.py -e instance_name=$instance_name -e NEXUS_USER=$NEXUS_USER -e NEXUS_PASSWORD=$NEXUS_PASSWORD -u ubuntu install_scheduler_to_instance.yaml

    ansible-playbook --private-key ~/.aws/aws_local.pem -i ec2.py -e instance_name=orbt-team -e NEXUS_USER=$NEXUS_USER -e NEXUS_PASSWORD=$NEXUS_PASSWORD -u ubuntu install_scheduler_to_instance.yaml
