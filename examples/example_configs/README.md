# Setting up config.yaml in Foundations

The goal of this document is to outline how Foundations uses a configuration-driven approach to deployment, and how to setup your configurations depending on where the execution environment(compute) will occur.

Configuration in Foundations is done through `config.yaml` files.

## Table of contents
[Vocabulary](#vocabulary)

[Types of Deployments](#types-of-deployments)

[Usage](#usage)

[Configuration Options](#configuration-options)

[Archive Configurations](#archive-configurations)

[Additional Configurations](#additional-configurations)

[Run script environment configs](#run-script-environment-configs)

[Using the config_manager](#using-the-config_manager)


## Vocabulary

It's important to understand the language used around deployment so that we can properly understand how models are run, and where.

Driver application: this where your code exist for using Foundations for both setting up stages and running them.

Execution environment: this is where models are computed i.e where jobs run.

Job: this is the unit used to describe the package that is the model, source code, and metadata that gets sent to be computed.

Deployment: you can think of deployment as how the job gets run (executed).

Queuing system: a way for multiple jobs to be sent to the execution environment, where they'll be put in line before they get run.

## Types of Deployments

You'll find example configurations for different deployment types in `/examples/example_config`.

Foundations works with three different types of deployments:

**Local Deployment:** this will run directly on the machine where the `.yaml` file is. This deployment doesn't require a queuing system. There are two versions of this, `local.config.yaml` for running on Linux and OSX, and `local_windows.config.yaml` for running on Windows.

**Google Cloud Platform (GCP) Deployment:** for use with Google's cloud service. A queuing system is required for use of this deployment configuration. When using this method of deployment, remember to authenticate with your Google Cloud service. Instructions on how to do this can be found [here](https://google-cloud.readthedocs.io/en/latest/core/auth.html).

**SSH Deployment:** this type of deployment uses a simple way of sending a job to a compute box and getting results. It expects to work with Foundations' SCP-style queueing system. 

The example folder contains seperate `_deploy` and `_results` config for _SSH Deployment_. This is because the SSH deployment initially stores the archives locally before sending it off remotely. With respect to workflow you can imagine using the deployment config with your code that's used for running a job––and using the results config to read results.

## Usage

You can specify the .config.yaml configuration file for your script using the `add_config_path` method in the `config_manager`. 
```
from foundations import config_manager

config_manager.add_config_path('config/local_default.config.yaml')
```
It is recommended that your `.config.yaml` file is not stored within the same directory as the script you're deploying. 

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

## Run script environment configs

Foundations creates its own virtual environment when running.  To set environment variables in that virtual environment, set the `run_script_environment` option.  This option is set by providing to it key-value pairs (where the key is the environment variable name and the value is the value to set in the variable):

```
run_script_environment:
    var0: value0
    var1: value1
    ...
```

The environment variables Foundations exposes are `log_level` and `offline_mode`.

### log_level

The `log_level` used here is for the `run.sh` script, including (for example) the output for `pip` when it installs libraries before running a submitted job.  The difference between this `log_level` and the one in the previous section is that this is for the `run.sh` script (i.e. everything the job requires in order to run) and is set under `run_script_environment`, while the previous `log_level` is for the Foundations job itself and has no parent configuration.

Allowed values for `log_level` are `INFO`, `ERROR`, and `DEBUG`, just as in the `log_level` option described in the previous section.  Leaving it unset is the same as setting `INFO`.  Setting any other value will disable all logging for all non-job-related processes.

### offline_mode

This variable is used to tell the `run.sh` that there is no internet.  This ensures that pip will not waste time trying to download packages when it can't.

Allowed values for `offline_mode` are `OFFLINE` and `FORCE_ONLINE`.  Setting any other value is the same as leaving it unset.  If unset, the `run.sh` will check for internet access before performing a `pip install`.  If this check fails, the `run.sh` will set `offline_mode` to `OFFLINE`.  If it succeeds, pip will be allowed to access the internet as necessary in order to download any python packages specified in your `requirements.txt`.

If `offline_mode` is set to `FORCE_ONLINE`, the connectivity check will be skipped and it will be assumed that we can `pip install` packages from the internet.

Keep in mind that if offline mode is set (either by you or by the `run.sh`) and pip finds a package in your `requirements.txt` that is not already on your system, job execution will correctly terminate with an error written to stderr.

### Using Redis for remote deployment

If you're running jobs using either SSH or GCP deployment, you'll need to set your Redis connection configuration. This can be done like so:

```
redis_url: redis://422.428.428.42:33333
```

If no `redis_url` value is set, it will default to `localhost:6379`.

### example run_script_environment

The below is for the case where you want `DEBUG`-level logging for `run.sh` processes and online mode:

```
run_script_environment:
    log_level: DEBUG
```

The below is for the case where you want `INFO`-level logging for `run.sh` processes and offline mode:

```
run_script_environment:
    log_level: INFO # can omit this line entirely - log_level is INFO by default!
    offline_mode: OFFLINE
```

## Using the config_manager

The `config_manager` can be used to override specific settings in default config specified in the `.config.yaml`. 

The general format of use:
`config_manager['<configuration>'] = <new config settings>`

### example changing log_level
The below could be used if you want to change the log_level in one of your experiments but don't want to modify your entire configuration.

```
from foundations import config_manager

config_manager['log_level'] = DEBUG
```

### example changing archive listing implementation
The below could be used to change the archive storage locations of one of your experiments. 
```
from foundations import config_manager, LocalFileSystemPipelineListing

config_manager['archive_listing_implementation'] = {
    'archive_listing_type': LocalFileSystemPipelineListing,
    'constructor_arguments': [/tmp/specialLocation],
}

```