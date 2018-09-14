# Setting up config.yaml in Foundations

The goal of this document is to outline how Foundations uses a configuration-driven approach to deployment, and how to setup your configurations depending on where the execution environment(compute) will occur.

Configuration in Foundations is done through `config.yaml` files.

## Vocabulary

It's important to understand the language used around deployment so that we can properly understand how models are run, and where.

Driver application: this where your code exist for using Foundations for both setting up stages and running them.

Execution environment: this is where models are computed i.e where jobs run.

Job: this is the unit used to describe the package that is the model, source code, and metadata that gets sent to be computed.

Deployment: you can think of deployment as how the job gets run (executed).

Queuing system: a way for multiple jobs to be sent to the execution environment, where they'll be put in line before they get run.

## Types of Deployments

You'll find a set of example configurations for different deployment types in `/examples/example_config`. For each type of deployment there's an example `_deploy` and `_results` config. With respect to workflow you can imagine using the deployment config with your code that's used for running a job––and using the results config to read results.

If no config is specified the application will try use all the configurations which will likely lead to unexpected failures.

Foundations works with three different types of deployments:

**Local Deployment:** this will run directly on the machine where the `.yaml` file is. This deployment doesn't require a queuing system.

**Google Cloud Platform (GCP) Deployment:** for use with Google's cloud service. A queuing system is required for use of this deployment configuration.

**Amazon Web Services (AWS) Deployment:** for use with Amazon's cloud service. A queuing system is required for use of this deployment configuration.  This has been tested using AWS Lambda + AWS Batch as the queuing + scheduling system.

**SSH Deployment:** this type of deployment uses a simple way of sending a job to a compute box and getting results. It expects to work with Foundations' SCP-style queueing system.

## Configuration Options

*Note: If no `config.yaml` is provided default values are used.*

All configurations take two arguments, `cache_type` (object), and `constructor_argument` (list). `constructor_argument` is how you can define the file path for any type of storage on the execution environment.

`constructor_argument` has different defaults depending on the type of deployment used. When using GCP deployment there is no default so `constructor_argument` will need to be defined for each configuration.

**cache_implementation**: Foundations uses caching to save time on rerunning stages that haven't changed, this configuration allows the integrator to define where caching should occur in the execution environment. The default value is `NullCacheBackend` which means no caching.

**archive_listing_implementation**: The archives listings configuration allows Foundations to specify how to list and enumerate items. The default value is `NullArchiveListing` which means no archiving is provided.

## Archive Configurations:

The below configurations allow Foundations to know where and how data is stored in the execution environment.

Default values for below parameters is `NullArchive` which means no archiving is provided.

**persisted_data_archive_implementation**: persisted data is how Foundations saves the returns value from a stage. If you want to run a job and see results, you'll need to persist the data and define where it should be saved.

**provenance_archive_implementation**: provenance is information about stage relationships that Foundations can save in order to have a historical record of how a series of stages ran.

**job_source_archive_implementation**: this is all the source code wrapped up in an archive object that will allow for a job to be fully reproducible. 

**artifact_archive_implementation**: this is how Foundations interacts with the model artifact for the job. Model artifacts are the way Foundations can save a model for later use.

**stage_log_archive_implementation**: stage logs are where you can save results from your model.

**miscellaneous_archive_implementation**: additional information about the job.

## Deployment Configurations:

**deployment_implementation**: defines either GCP, local, or SSH type deployment. The default is `LocalShellJobDeployment` which means it will use current working directory.


## Additional Configurations

For SSH deployments you'll need to define some additional values so that Foundations is able to SSH into the execution environment. Here's an example usage:

```
remote_user: lou

remote_host: 422.428.428.42

port: 22222

shell_command: /bin/bash

code_path: /home/lou/mount/testbed/jobs

result_path: /home/lou/mount/testbed/results

key_path: <key_path>

log_level: DEBUG
```

Just like with SSH the `remote_user` and `remote_host` value will be the login for the execution environment machine.  The `port` entry specifies what port the SSH service is listening to on the remote machine.  It is optional - not specifying it will give it the default of 22.

`shell_command`: needed for the queuing system to know how to run a `.sh` file. This is a necessary configuration as different platforms require different paths to running shell scripts.

`code_path`: the directory where jobs should be stored.

`result_path`: the directory where job results should be stored after they've been run.

`key_path`: the private key necessary for using SSH.

`log_level`: for debugging purposes if set to `DEBUG` Foundations will be verbose in its output. Remove this configuration will turn off debug mode and will default to using `INFO`. This is a wrapper on top of Python's logging.