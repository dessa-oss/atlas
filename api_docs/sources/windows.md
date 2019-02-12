<h1>Windows Instructions</h1>

**Read [the start guide](../start_guide/) first if you haven't already**

### Windows

You will need to install [git bash](https://git-scm.com/download/win) and [anaconda](https://conda.io/miniconda.html).
To run Foundations correctly, you will need to run all comands from an Anaconda prompt.

To install:

- Open an Anaconda prompt
- create a new conda environment by running
```
conda create --name found-env python=3.6
```
- activate the environment by running
```
conda activate found-env
```
- install dependencies via pip
```
pip install dill PyYAML pandas pysftp paramiko flask-restful Flask-Cors google-api-python-client google-auth-httplib2 google-cloud-storage futures promise
```
- install foundations libraries via pip using the [Wheel installation](../start_guide/#wheel-installation)

There are more steps to consider to make Foundations run successfully on Windows. See these [instructions here](../windows/) for more details.


## Setting up local configuration

In order to get Foundations working correctly on Windows, you'll have to ensure that you environment is set up correctly. When installing software dependencies (such as Anaconda or Git), the default installation settings should be sufficient to get things working.

### Deploying jobs
As per [the start guide](../start_guide/#environment-and-dependencies) you should able to use an example configuration to start deploying jobs using Foundations.

The most important change in any configuration is the `shell_command` key. Setting this value allows Foundations to be able to understand how to execute the shell scripts that are required for running jobs. The recommended value for this is `C:\\Program Files\\Git\\bin\\bash.exe` which is in the default install location for git for Windows. If you changed this path during installation, you will have to change this value respectively.

### Local deployment
```yml
cache_implementation:
  cache_type: foundations_contrib.local_file_system_cache_backend.LocalFileSystemCacheBackend
  constructor_arguments: ["C:\\foundations\\foundations-cache"]

archive_listing_implementation:
  archive_listing_type: foundations_contrib.local_file_system_pipeline_listing.LocalFileSystemPipelineListing
  constructor_arguments: ["C:\\foundations\\foundations-archive"]

stage_log_archive_implementation: &archive_implementation
  archive_type: foundations_contrib.local_file_system_pipeline_archive.LocalFileSystemPipelineArchive
  constructor_arguments: ["C:\\foundations\\foundations-archive"]

persisted_data_archive_implementation: *archive_implementation
provenance_archive_implementation: *archive_implementation
job_source_archive_implementation: *archive_implementation
artifact_archive_implementation: *archive_implementation
miscellaneous_archive_implementation: *archive_implementation

project_listing_implementation:
  project_listing_type: foundations_contrib.local_file_system_pipeline_listing.LocalFileSystemPipelineListing
  constructor_arguments: ["C:\\foundations\\projects"]

deployment_implementation:
  deployment_type: foundations_contrib.local_shell_job_deployment.LocalShellJobDeployment

redis_url: redis://localhost:6379

shell_command:
  "C:\\Program Files\\Git\\bin\\bash.exe"
```

The example configuration above can be used as a starting point for running jobs locally on Windows. Please take note that when running jobs locally on Windows, all paths must be prefixed by the Windows partition (ie `C:\\`) that they are located on.

### Deploying remote jobs from Windows
It is also important to understand that if you are deploying from Windows to the Foundations scheduler that the paths defined in you configuration must retain their Linux form. For example, we would use `/path/to/remote/jobs` instead of `C:\path\to\remote\jobs`
