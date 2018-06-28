# Pipeline deployment

## Installing dependencies

Currently, vcat has no dependencies, but must be installed on the client's (user's) machine via pip. To create a pip wheel, one may run `vcat_sdk/build.sh` and install the resulting wheel from the `vcat_sdk/dist` directory.

After this, the module may be imported like so:

 ```python
 from vcat import *
 ```

## Folder Structure

Projects may now be deployed outside the `vcat` project directory, assuming `vcat` is properly installed. Your project structure can be whatever you want; `vcat` will be able to bundle your entire project directory.

## Workflow

### Python Code

Given a pipeline `pipe`, one may run the following to deploy the pipeline locally:

```python
deployment = pipe.run()
# deployment.wait_for_deployment_to_complete()
# result = deployment.fetch_job_results()
result = deployment.fetch_job_results()
print(result)
```

### Configuration YAML

```
# local_deploy.config.yaml
# must be in same directory as where the above code is being run

# default of local shell job deployment

cache_implementation:
  cache_type: vcat.LocalFileSystemCacheBackend
  constructor_arguments: [/tmp/foundations-cache]

archive_listing_implementation:
  archive_listing_type: vcat.LocalFileSystemPipelineListing
  constructor_arguments: [/tmp/foundations-archive]

stage_log_archive_implementation:
  archive_type: vcat.LocalFileSystemPipelineArchive
  constructor_arguments: [/tmp/foundations-archive]

persisted_data_archive_implementation:
  archive_type: vcat.LocalFileSystemPipelineArchive
  constructor_arguments: [/tmp/foundations-archive]

provenance_archive_implementation:
  archive_type: vcat.LocalFileSystemPipelineArchive
  constructor_arguments: [/tmp/foundations-archive]

job_source_archive_implementation:
  archive_type: vcat.LocalFileSystemPipelineArchive
  constructor_arguments: [/tmp/foundations-archive]

artifact_archive_implementation:
  archive_type: vcat.LocalFileSystemPipelineArchive
  constructor_arguments: [/tmp/foundations-archive]

miscellaneous_archive_implementation:
  archive_type: vcat.LocalFileSystemPipelineArchive
  constructor_arguments: [/tmp/foundations-archive]

job_source_bundle:
  bundle_name: test_bundle
  target_path: .

```
Which should print the result of the deployed job to `STDOUT`

## What happens under the hood

### Bundling a job

- `vcat` reads a YAML file containing configs re: where to run the job and put the results
- `vcat` serializes a job and it's configuration
- `vcat` bundles the job directory (current working directory)
- `vcat` bundles the `vcat` module
- `vcat` bundles additional resources from the module required to run as standalone (such as `main.py`, `run.sh`, etc.)
- A `tgz` file is created in the parent directory of the job directory with the name of the job (as specified by the python script deploying the job). This is the bunle and contains all files required to run the job

## Running the job

`vcat` uses the specified deployment method (in the example, a local shell based job deployment) which then sends the bundled job where it is needed, extracts it and then runs the job via a shell script.

After the job is been deployed, the bundle is cleaned up

