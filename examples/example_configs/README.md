# Setting up config.yaml in Foundations

The goal of this document is to outline how Foundations uses a configuration-driven approach to deployment, and how to setup your configurations depending on where the execution environment(compute) will occur.

Configuration files should not done by machine learning engineers, and should instead be implemented by the network's integration engineer––that said the examples in this directory should hopefully give some guidance in best practices for configurations.

Configuration in Foundations is done through `config.yaml` files.

## Vocabulary

It's important to understand the language used around deployment so that we can properly understand how models are run, and where.

Driver application: think of this as the Python code that defines the stages, and runs (in the `.run()` sense) the job.

Execution environment: this is where models are computed. Could be GCP, or even a DGX!

## Types of Deployments

Foundations works with three different types of deployments:

**Local Deployment:** this will run directly on the machine where the `.yaml` file is. It should be noted that this deployment doesn't require a queuing system–-this is mainly used for testing and development purposes.

**Google Cloud Platform (GCP) Deployment:** for use with Google's cloud service. A queuing system is required for use of this deployment configuration.

**SSH Deployment:** this type of deployment is used at a few clients. It's a simple way of sending a job to a compute box and getting results. It expects to work with our SCP-style queueing system.



## Configuration Options

*Note: If no `config.yaml` is provided default values are provided.*

All configurations take two arguments, `cache_type` (object), and `constructor_argument` (list). `constructor_argument` is how you can define the file path for any type of storage on the execution environment.


**cache_implementation**: Foundations uses caching to save time on rerunning stages that haven't changed, this configuration allows the integrator to define where caching should occur in the execution environment.

**archive_listing_implementation**: The archives listings configuration allows Foundations to specify how to list and enumerate items within archive storage

## Archive Configurations:

The below configurations allow Foundations to specify how the different pieces of information, whether that be source code with `job_source_archive` or stage relationships with `provenance_archive_implementation`, are store and where in the execution environment.

**persisted_data_archive_implementation**: persisted data is how Foundations save the return returns from a stage.

**provenance_archive_implementation**: provenance is information about stage relationships that Foundations uses.

**job_source_archive_implementation**: job source is where the source code lives for a job.

**artifact_archive_implementation**: this is how Foundations interacts with the model artifact for the job.

**miscellaneous_archive_implementation**: additional information about the job.


## Additional Configurations

For SHH deployments you'll need to define some additional values so that Foundations is able to SSH into the execution environment. Here's an example usage:

```
remote_user: lou

remote_host: 422.428.428.42

shell_command: /bin/bash

code_path: /home/lou/mount/testbed/jobs

result_path: /home/lou/mount/testbed/results

key_path: <key_path>
```