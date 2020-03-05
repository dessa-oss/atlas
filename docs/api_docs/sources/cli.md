# CLI Reference

## Introduction

The `foundations` CLI is one of the primary methods of of creating, deploying, and interacting with `foundations` jobs, apart from the GUI.

Quick information on these commands can be found by running `foundations --help`.

---

## Commands

### `foundations init`

```bash
foundations init <project-name>
```

This is the recommended way of creating a `foundations` project. A directory will be created containing files for an example `foundations` project with default configuration and source code.

**Positional Arguments**

* **`project_name`**: The name of the directory to be created.

---

### `foundations submit`

```bash
foundations submit
    [--entrypoint ENTRYPOINT]
    [--project-name PROJECT_NAME]
    [--num-gpus NUM_GPUS]
    [--ram RAM]
    [--stream-job-logs STREAM_JOB_LOGS]
    <scheduler-config>
    <job-dir>
    <command>
```

This submits a `foundations` job to the scheduler. Running this command will add the job to the scheduler's wait queue, after which it will be run.

**Positional Arguments**

* **`scheduler-config`**: Specifies which scheduler submission configuration to use. `scheduler` is the default configuration.
* **`job-dir`**: The path to the `foundations` project. This can be a relative or absolute path.
* **`command`**: The arguments passed in to the entrypoint. This is usually a path to a file to run. This corresponds to the concept of a `CMD` in Docker.

**Optional Arguments**

* **`--entrypoint`**: The command to run the job. This defaults to `python`, and corresponds to the concept of `ENTRYPOINT` in Docker.
* **`--project-name`**: The name of the project that this job belongs to. By default, this is the name of the project directory.
* **`--num-gpus`**: Specifies the number of GPUs to be allocated when running a job. By default 0 GPUs are specified.
* **`--ram`**: The amount of RAM (in GB) to allocate to running this job. By default, there is no limit on the amount of RAM a job can use.
* **`--stream-job-logs`**: Whether to stream the logs from the running jobs into the current terminal. This is true by default.

---

### `foundations get job`

```bash
foundations get job
    [--save_dir SAVE_DIR]
    [--source_dir SOURCE_DIR]
    <scheduler-config>
    <job-id>
```

Downloads the entire job bundle for a specified job. This is usually the project directory of the job that was submitted, containing the job's source code and configuration files. By default, the downloaded bundle is in the form of a directory named `job-id`.

**Positional Arguments**

* **`scheduler-config`**: The scheduler of which the job to download is in.
* **`job-id`**: The ID of the job to download the bundle of.

**Optional Arguments**

* **`--save_dir`**: The path on your local machine to download the job bundle to. This defaults to the current directory.
* **`--source_dir`**: The relative directory path to download artifacts from. Default will download all artifacts from job.

---

### `foundations get logs`

```bash
foundations get logs <scheduler-config> <job-id>
```

Outputs the logs of a specified job. This is useful for debugging a job that failed, or for gaining more information into what happened in a particular job.

**Positional Arguments**

* **`scheduler-config`**: The scheduler of which to retrieve logs for a job.
* **`job-id`**: The ID of the job to get logs of.


---

### `foundations stop`

```bash
foundations stop <scheduler-config> <job-id>
```

This stops the running job specified with the ID `job-id`. Stopped jobs are given a status of `failed`. This command cannot be applied to non-running jobs.

**Positional Arguments**

* **`scheduler-config`**: The scheduler of which the job to be stopped is running in.
* **`job-id`**: The ID of the job to be stopped.

---

### `foundations clear-queue`

```bash
foundations clear-queue <scheduler-config>
```

This removes all scheduled jobs from the queue specified by `scheduler-config`.

**Positional Arguments**

* **`scheduler-config`**: The scheduler of which to clear the queue.

---

### `foundations delete job`

```bash
foundations delete job <scheduler-config> <job-id>
```

Deletes a specified job. Deleting only works for failed or completed jobs.

!!! note
    This will ask for your password as we are deleting a protected directory.

**Positional Arguments**

* **`scheduler-config`**: The scheduler of which to delete a job.
* **`job-id`**: A specific job ID. Find the job ID in the job listings page in the GUI.

**Optional Arguments**

These are optional arguments global to all commands.

* **`-h`**: Shows a help message and exits.

* **`--debug`**: Sets debug mode, which allows stack traces and other information useful for debugging to be displayed on the terminal.