<h1>Setup for Deploying Jobs to Remote Environments</h1>

In this example, we will demonstrate how to setup job deployments to different remote environments. We will be using the [MLP Neural Network](../mnist_example/) as our model code, so it is highly recommended to look at the example before following this example.

The project directory structure should look like this to run the model correctly:
```
mnist_example
├── config
│   ├── remote.config.yaml
│   └── local.config.yaml
├── data
├── post_processing
│   └── results.py
├── project_code
│   ├── driver.py
│   └── model.py
├── requirements.txt
└── README.txt
```
---
##1. Specify Remote Environment Configuration 

When a new project is created using the `init` CLI command, Foundations will automatically generate a local environment configuration file for deploying jobs on the local machine. In order to deploy to other environments, additional environment configuration files will need to be defined for Foundations to know where and how (credentials) to bundle jobs. This will vary greatly depending on how the Foundations infrastructure is setup. Let's create a new configurations file in the `config` directory and call it `remote.config.yaml`:
```
job_deployment_env: <local/aws/gcp/ssh>
results_config:
  redis_end_point: <path/to/redis>
  archive_end_point: </path/to/archives>
cache_config:
  end_point: </path/to/cache>

ssh_config:
  host: <foundations>
  port: <default 22>
  code_path: </path/to/job/storage>
  result_path: </path/to/results/storage>
  key_path: <local/path/to/private/key>
```

Here, you will specify the paths of the remote environment for storing cached results, jobs, and redis as well as credentials for SSH, GCP and AWS deployments. More information on the different parameters can be found [here](../configs/#configuration-options).

##2. Specify Additional Remote Dependencies

When developing a model, additional python packages and modules are required. It's easy to install these packages locally with `pip` or Anaconda, but these packages may not necessarily exist on the remote environments where jobs are being run. Foundations allows users to specify mandatory additional packages via a `requirements.txt` file in the project directory. In this file, users can specify libraries, which they've used locally to develop the model, as well as specific versions for the remote environment to download and have available for the job to run smoothly.

In the MNIST example, we use keras, tensorflow, and numpy as part of the model. In order to ensure the remote environment has the necessary packages, we create a `requirements.txt` file in the project root directory with the following:
```
numpy
keras
tensorflow
```
This will indicate to Foundations to `pip install` these packages in a virtual environment on the remote machine before running the job. If specifc versions are needed, they can be specified as such:
```
numpy==1.15.2
keras==2.2.4
tensorflow==1.11.0
```
**NOTE:** Specifying additional packages using `requirements.txt` only works for remote environments that have internet access. Depending on the infrastructure, this may not be the case. In this case, the remote environment will need to be setup prior with the necessary packages and only those will be available for running jobs.

##3. Deploy the Job to Remote Environment

Now we're ready to deploy the model to the remote environment! To view the new remote environment, in the project root directory, run:
```bash
$ foundations info --env
```

This will list all available deployment environments. You should expect to see the following:
```bash
$ foundations info --env
"""
global configs:
env_name    env_path
----------  ----------

project configs:
env_name    env_path
----------  ------------------------------------------------------------------------
local       /path/to/project/config/local.config.yaml
remote      /path/to/project/config/remote.config.yaml
"""
```
You can see that we now have two available environments: local and remote. 

To run the model on the remote env, we will use the Foundations CLI `deploy` command. This will bundle all files within the project directory and push them to the remote environment, specified by the configuration file. In the project root directory run:
```bash
$ foundations deploy project_code/driver.py --env=remote
"""
2019-03-25 16:09:23,330 - foundations.stage_connector_wrapper - INFO - Deploying job...
2019-03-25 16:09:28,143 - foundations_contrib.config_manager - INFO - Configured with {'deployment_type': <class 'foundations_ssh.sftp_job_deployment.SFTPJobDeployment'>}
2019-03-25 16:09:28,710 - foundations_internal.deployment_manager - INFO - Job '08454775-c1d3-4769-828c-47dfe11f745c' deployed.
"""
```

