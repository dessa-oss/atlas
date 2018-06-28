# Project V

## Integration Guide

Project V helps create reproducible and organized machine learning pipelines. It also helps centralize the storage of logs and outputs of these machine learning pipelines, and it enables quick, programmable retrieval of these pieces of information. This guide outlines what python classes need to be implemented in order to integrate Project V.

In the following, the user is the individual who's performing the Project V integration.

Note only Python 3 is currently supported.

## Overview
The user needs to implement the following four components:

1. Job deployment: how a job is submitted to a user-provided scheduler to run
    * A `Deployment` class gives access to execution environment
2. Job Listing: occurs with deployment, to log results after execution
    * `Listing` classes will allow user to interact with jobs
3. Reading results: how the user is able to access jobs and their results
    * `PipelineArchive` classes will be used to store results
4. Caching: how the system reduces duplicate runs
    * `CacheBackend` classes will allow the system to have a caching layer to optimize job run speed


1. Job Deployment: submit jobs
    * For Job Deployment a installer will need to implement:
        * An adapter that give access to the execution environment (Deployment class talks with the scheduler)
            * This class helps define where and how the jobs will be submitted
            * A check to see if jobs are completed
            * A way to fetch results
            * A deployer for handling all jobs (e.g.: GCP, driver)
        * The execution environment (e.g.: Fei-Fei)
            * The execution environment includes things like the job scheduler, master, and workers
            * While this guide doesn't go into detail about building a scheduler (queuing system) it relies on it in order to successfully run jobs

    * How does deployment work?
        * A pipeline and arguments are submitted in the form of a job to the deployer
        * Configurations set by the installer tell the system where to deploy
        * Configurations set by the user tell the system where to cache and send results
    * The deployment class determines where / how to deploy
        * The deployer then pushes a job to an execution environment that runs `run.sh` and `main.py` for the job
        * A installer defined `is_job_complete` is constantly checking to see if results have come back from submitted jobs
        * A installer defined `fetch_job_results` allows the system to get results when `is_job_complete` returns `true`
    * `fetch_job_results` returns a results object, which is a pipeline context in dict form for a specific job
        * Note: use `fetch_job_results` to see them immediately after the job has run––the main way to view results is through the `ResultsReader`




The following methods describe how job are deployed and then results fetched.

Requirements:

* `__init__(self, job_name, job, job_source_bundle)`
    * Where initial setup of config, job naming, job bundler, and job results are done
    * `job_name`: string, name of the job to run
    * `job`: Job object (class defined by SDK).  See Appendix for more information.
    * `job_source_bundle`: a JobSourceBundle object (class defined by SDK).  See Appendix for more information.
* `config(self)`
    * Returns: configuration object
* `job_name(self)`
    * Returns: job name
* `deploy(self)`
    * Runs the job and then cleans up after it has been deployed
    * Doesn’t return anything
    * Job will be submitted to the execution environment here
* `is_job_complete(self)`
    * Checks if job has completed (will not exist if job has failed)
    * Returns: true or false depending on whether job is finished running
* `fetch_job_results(self)`
    * Functions as main way to get job output from storage
        * The type of "output" will be defined by the configuration, which is decided by the installer
    * Returns: job object for a specific job


## 2. Job Listing
How and where are job and their results are tracked

* For writing results, an installer will need to implement
    * A `Listing` class that lists jobs
* How does writing on completion work?
    * A user will use the `Listing` class to define where the completed job will be stored
* If implementation is not possible with Listing some other type of record keeping will need to be customer created in order to keep track of jobs

Requirements:
* `track_pipeline(self, pipeline_name)`
    * Take the pipeline name and saves it to a registry (e.g.: could be on storage, or in memory)
* `get_pipeline_names(self)`
    * Gives all pipeline names
    * Returns: list of pipeline names


## 3. Reading results
The pipeline archive is an abstraction layer on top of storage. Provides read/write functionality to some type of storage for job results.


For reading from the pipeline archive a installer will need to implement:

* A PipelineArchive class that can be used by the user as an adaptor to components of the job
    * Each component can have its own PipelineArchive instance
    * `stage_log_archive`
        * Where results of job are stored, such as metrics
    * `persisted_data_archive`
        * Where data is stored after calling persist on a pipeline
    * `provenance_archive`
        * Where job provenance is stored
    * `job_source_archive`
        * Where source job folder is stored, which includes source code, data, etc
    * `artifact_archive`
        * Where additional files from running a job are stored
    * `miscellaneous_archive`
        * Where metadata (and anything else the user may require) about running the job is stored


Requirements:

* `__enter__(self)`
    * Eg: opening a database connection
    * Eg: opening a file
    * Eg: creating a network socket
    * Used to allocate a system resource
    * Anything the remote would need to do to start reading data
    * Returns: self
* `__exit__(self, exception_type, exception_value, traceback)`
    * Allows for cleanup when done with system resource
* `append(self, name, item, prefix=None)`
    * Intention: take a python object (e.g.: provenance, stage context, pipeline context...etc) and stores it in a given location
    * Does not return anything
* `append_binary(self, name, serialized_item, prefix=None)`
    * Instead of taking a python object, takes a raw binary string (e.g.: the output of .dumps() for pickle) and stores in a given location
    * Does not return anything
* `append_file(self, file_prefix, file_path, prefix=None, target_name=None)`
    * Takes a file and sends to storage
    * Does not return anything
* `fetch(self, name, prefix=None)`
    * Ability to get python object from storage
    * Returns: deserialized python object, otherwise None
* `fetch_binary(self, name, prefix=None)`
    * Ability to get raw binary string from storage
    * Returns: serialized python object (binary string), otherwise None
* `fetch_from_file(self, file_prefix, file_path, prefix=None, target_name=None)`
    * Ability to get file from storage
    * Doesn’t return anything, but downloads to local storage


## 4. Caching
For caching what needs to be implemented:

* To enable use of a caching layer, a CacheBackend class should be implemented
* This will allow the system to use the output of a stage that has previously run


How does the caching layer work?

* While processing jobs the execution environment checks the cache to see if a stage has been run before
* The cache store is where cache is held and retrieved from when a stage is run more than once across job runs


Requirements:

* `get(self, key)`
    * Allows system to get cached data
    * Return value at key if key exists in cache, otherwise return None
* `set(self, key, value)`
    * Allows system to add to cached data 
    * Add value at key into cache
    * Doesn't return anything

## Configuration
All the configuration is handled by project V, but can be overridden if needed. The configuration interface is a dictionary.

Necessary configuration by installer. For all configurations a python type that implements that interface in needed, as well as all arguments that are passed to construct that type.

* `cache_implementation`
* `archive_listing_implementation`
* `stage_log_archive_implementation`
* `persisted_data_archive_implementation`
* `provenance_archive_implementation`
* `job_source_archive_implementation`
* `artifact_archive_implementation`
* `miscellaneous_archive_implementation`
* `deployment_implementation`

Example config:

```
deployment_config = {
    'cache_implementation': {
        'cache_type': GCPCacheBackend,
    },
    'archive_listing_implementation': {
        'archive_listing_type': GCPPipelineArchiveListing,
    },
    'stage_log_archive_implementation': {
        'archive_type': GCPPipelineArchive,
    },
    'persisted_data_archive_implementation': {
        'archive_type': GCPPipelineArchive,
    },
    'provenance_archive_implementation': {
        'archive_type': GCPPipelineArchive,
    },
    'job_source_archive_implementation': {
        'archive_type': GCPPipelineArchive,
    },
    'artifact_archive_implementation': {
        'archive_type': GCPPipelineArchive,
    },
    'miscellaneous_archive_implementation': {
        'archive_type': GCPPipelineArchive,
    },
    'deployment_implementation': {
        'deployment_type': SSHJobDeployment
    },
    'remote_user': 'thomas',
    'remote_host': 'localhost',
    'shell_command': '/bin/bash',
    'code_path': '/home/thomas/Dev/Spiking/vcat-results/tmp/code',
    'result_path': '/home/thomas/Dev/Spiking/vcat-results/tmp/results',
    'key_path': '/home/thomas/.ssh/id_local',
}
```


## Final Integration Steps
* Once all classes have been implemented you'll need to consider the following depending on your system architecture
* Where should Project V sit?
    * Machine learning engineers will use the source code along with Project V to build and run pipeline for their models, so this module will need to be accessible on their client machines

## Appendix - SDK Classes Quick Reference
What follows is a (very) quick overview of the classes with which one will need to interact---__but not implement__! - when creating an integration. Only relevant methods will be shown.

### Job
This class contains the pipeline to run as well as any parameters to insert into the pipeline.

* `run(self)`
    * Runs the job's pipeline using the parameters packaged with the job.
    * Does not return anything. All results will be automatically sent to the PipelineArchives defined within the (end-user-supplied) configurations.
    * The results will also be contained within a pipeline context object (see next method)
* `pipeline_context(self)`
    * Returns the Job's pipeline context, which functions as an aggregator for pipeline run output as well as where the (end-user-supplied) configurations are stored.
* `deserialize(serialized_self)`
    * Static method
    * Takes a dill-serialized Job object and returns the deserialized Job object. Dill serialization is done with protocol=2.

### JobSourceBundle
This class contains functionality for bundling and un-bundling the source code used to create a Job.

* `__init__(self, bundle_name, target_path)`
    * Constructor that takes a bundle name (string) which defines the name of the job source archive as well as a target path (string) which defines where to unpack the archive

* `bundle(self)`
    * Creates an archive containing all files in the directory named by target_path (taken in by the constructor above). The archive is given the name <bundle_name>.tgz (bundle_name also taken in by the constructor above)
* `unbundle(self, path_to_save)`
    * Extracts the archive named by bundle_name to the directory named by path_to_save
* `cleanup(self)`
    * Deletes the archive named by bundle_name, but not the files used to create it (i.e. files in target_path)