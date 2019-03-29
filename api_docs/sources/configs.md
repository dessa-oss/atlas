<h1>Setting Up Different Deployment Environments in Foundations</h1>

Foundations uses a configuration-driven approach to deployment, and which configurations are selected when deploying a job determines where the execution environment(compute) will occur.

Configuration in Foundations is done through `config.yaml` files.

## Concepts and Vocabulary

It's important to understand the language used around deployment so that we can properly understand how models are run, and where.

**Driver Application**: this where your code exist for using Foundations for both setting up stages and running them.   

**Execution Environment**: this is where models are computed (ie: where jobs run). This can be a variety of different locations such as local (where you run model code on your local machine), or on a remote server (Google Cloud Platorm, Amazon Web Services, other SSH servers). See below for more details on Types of Deployments.

**Job**: this is the unit used to describe the package that is the model, source code, and metadata that gets sent to be computed.  

**Deployment**: you can think of deployment as how the job gets run (executed).  

**Queuing System**: a way for multiple jobs to be sent to the execution environment, where they'll be put in line before they get run.  

## Types of Deployments

Foundations works with a few different types of deployment options:

**Local Deployment:** this will run directly on the machine where the `.yaml` file is. This deployment doesn't require a queuing system. There are two versions of this, `local.config.yaml` for running on Linux and OSX, and `local_windows.config.yaml` for running on Windows.

**Google Cloud Platform (GCP) Deployment:** for use with Google's cloud service. A queuing system is required for use of this deployment configuration. When using this method of deployment, remember to authenticate with your Google Cloud service. Instructions on how to do this can be found [here](https://google-cloud.readthedocs.io/en/latest/core/auth.html).

**Amazon Web Services (AWS) Deployment:** for use with Amazon's cloud service. A queuing system is required for use of this deployment configuration. When using this method of deployment, remember to authenticate with your AWS service. Instructions on how to do this can be found [here](https://docs.aws.amazon.com/codedeploy/latest/userguide/auth-and-access-control.html).

**SSH Deployment:** this type of deployment uses a simple way of sending a job to a compute box and getting results. It expects to work with Foundations' SCP-style queueing system. 

To select which of the above to deploy a job to, users specifiy different configuration files which contain parameters and additional information so that Foundations can properly access and run model code on the environment.

## How to Deploy

Configuration files can live both globally on the machine or locally per Foundations project. When using the `foundations init` command, a default configuration file is [automatically created](../project_creation/#project-creation) in the `/config` directory. To set global environments, add `*.config.yaml` files to `~/.foundations/config`. You may need to create this directory first with:

```bash
mkdir ~/.foundations/config
```

Jobs can then be deployed to different environments in two ways:

<h3>1. Using the Foundations CLI</h3>
In the Foundations project root directory, running the following command will deploy jobs to user-specified environments:
```shellscript
$ foundations deploy <relative_path_to_driver_file>.py --env=<env_name>
```
Foundations will first look for any `<env_name>.config.yaml` file in the `/config` directory that matches the specified `--env` argument. If a matching configuration file is found, Foundations will deploy the job to that specified environment. Otherwise, it will then look for the configuration in the global directory `~/.foundations/config` . If no configuration files are found, the command will return an error.

Available configuration files (and environments) can be found using:
```shellscript
$ foundations info --env
```

For more information on the Foundations CLI, please refer to the documentation [here](../project_creation/)

**Note:** If your code contains setting the environment via the notebook instructions below, this **will** override the selected environment by the deploy command.

<h3>2. Using Notebooks</h3>

When using a notebook such as Jupyter to develop your model code, you can deploy jobs by running any stage that calls the `.run()` function. However, you will first need to specify the deployment environment for your notebook using the `set_environment` function. 
```
import foundations

foundations.set_environment('local')
```
If choosing to deploy this way, the notebook will have to be situated in the project root directory and any functions imported from relative files will need to be specified accordingly. For more information on setting environments, please refer documentation [here](../set_deployment_env/).

## Configuration Options

*Note: Typically, the Dessa team will provide tested and properly setup configuration files for deployment to the different environments which will not require users to modify any configuration options. In addition, if no `config.yaml` is provided, then Foundations will use built-in default values for job deployments*

### Define Environment 

**job_deployment_env**: specifies what to label the environment as for deploying jobs. You can view all available all environments with the [Foundations CLI](../configs/) command: `foundations info --env`

### Results Configurations

```json
'results_config': {
    'archive_end_point': '/path/to/archives',
    'redis_end_point': 'redis://someredis'
},
```

**archive_end_point**: defines full path to where to store results. The default is `local` which means it will use current project directory.

**redis_end_point**: redis endpoint where we want to store results for faster reading

### Cache Configurations

```json
'cache_config': {
    'end_point': '/path/to/the/cache'
},
```

**end_point**: defines full path to where to store cache files. The default is `local` which means it will use current project directory.

### Additional Configurations

For any SSH deployment (including GCP and AWS) to remote addresses, you'll need to define some additional values so that Foundations is able to SSH into the execution environment. Here's an example usage:

```json
'ssh_config': {
    'user': lou
    'host': '11.22.33.44',
    'port': 2222
    'key_path': '/path/to/the/keys',
    'code_path': '/path/to/the/code',
    'result_path': '/path/to/the/result',
}
```
**user** (*optional*): what user profile to access the remote server as. By default, it will use `foundations`.  
**host** (*required*): the remote machine ip address.  
**port** (*optional*): specifies what port the SSH service is listening to on the remote machine. By default uses port 22.  
**key_path** (*required*): the private key necessary for using SSH.   
**code_path** (*required*): the directory where jobs should be stored.   
**result_path** (*required*): the directory where job results should be stored after they've been run.  

<h3>log_level</h3>

Allowed values for `log_level` are `INFO`, `ERROR`, and `DEBUG`, just as in the `log_level` option described in the previous section.  Leaving it unset is the same as setting `INFO`.  Setting any other value will disable all logging for all non-job-related processes.