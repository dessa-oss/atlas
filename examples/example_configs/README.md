# Setting up config.yaml in Foundations

The goal of this document is to outline how Foundations uses a configuration-driven approach to deployment, and how to setup your configurations depending on where the execution environment(compute) will occur.

Configuration files should not done by MLEs, and should instead be implemented by the network's integration engineer––that said the examples in this directory should hopefully give some guidance in best practices for configurations.

Configuration in Foundations is done through `config.yaml` files.

## Vocabulary

It's important to understand the language used around deployment so that we can properly understand how models are run, and where.

Driver application: think of this as the Python code that defines the stages, and runs (in the `.run()` sense) the job.

Execution environment: this is where models are computed. Could be GCP, or even a DGX!

## Types of Deployments

Foundations works with three different types of deployments:

Local Deployment: this will run directly on the machine where the `.yaml` file is. It should be noted that this deployment doesn't require a queuing system–-this is mainly used for testing and development purposes.

Google Cloud Platform (GCP) Deployment: for use with Google's cloud service. A queuing system is require for use of this deployment configuration.

SSH Deployment: this type of deployment is used at a few client premises. It's a simple way of sending a job to a compute box and getting results. It expects to work with our SCP-style queueing system.




## Configuration Options

All configurations take two arguements, `cache_type` (object), and `constructor_argument` (list)


*cache_implementation*: defines what cache type to use


*archive_listing_implementation*: defines what archive listing type to use

*persisted_data_archive_implementation*: defines what persisted data archive

*provenance_archive_implementation*:

*job_source_archive_implementation*:

*artifact_archive_implementation*:

*miscellaneous_archive_implementation*:
