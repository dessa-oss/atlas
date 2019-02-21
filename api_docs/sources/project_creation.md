<h1>Foundations CLI Tool</h1>

The Foundations Command Line Tool provides users with a simple way to interact and manage projects in Foundations. The supported functionalities are listed below.

#Project creation#

The best way to start using Foundations is by creating a project using the Foundations command line tool.

```shellscript
$ foundations init <project_name>
```
Creates a project, which is basically a directory named after the specified project name with various sub-directories organized in a way that is useful for having a well-structured Machine Learning solution, as it's shown in the following graph:

```
project_name
├── config
│   └── default.local.yaml
├── data
├── post_processing
│   └── results.py
├── project_code
│   ├── driver.py
│   └── model.py
└── README.txt
```
The `config` directory is intended to be the place where configuration resides. A default configuration file is created inside it named `default.local.yaml` which contains a standard configuration for a local shell deployment.

The `data` directory is intended as a place to put the data the user's model requires as input.

The `project_code` directory contains two Python modules intended to be the files where the user's solution main code resides. The module file named `model.py` is where Python functions that make up the user's model should be defined. Each function there can be considered as a step (stage) towards building a model and can be imported later into the `driver.py` file to be invoked as a Foundations' stage. Of course, there could be more than just one source code file like `model.py`. The `driver.py` file is the main script that should be executed by the user and where stage creation and execution should happen.

The `post_processing` directory is where the user writes some code to interact with results that are available in the execution environment. By default a `results.py` script is created with some basic functionality to obtain metrics for all jobs.

At the root of the project's directory there is a `README.txt` file that explains the project structure just as this page does.

---
#Deploying Jobs#

The Foundations CLI makes it easy to deploy jobs to different environments across different projects. 

```shellscript
$ foundations deploy <relative_path_to_driver_file>.py --env=<env_name>
```

Running this command in the project base directory will deploy the model to the specified environment. For example, in the directory structure below, run this command within the `project` directory. If the command is not run within the project directory, it will return an error message.

```
project
├── config
│   └── local.config.yaml
├── project_code
    ├── driver.py
```

To deploy the driver in the above example, run:
```shellscript
$ foundations deploy project_code/driver.py --env=local
```

**Note:** Ensure your `driver_file` does not include the following header, otherwise you will get an error:
```python
if __name__ == "__main__":
    etc.
```
---
#Retrieve Environment Information#

Users can setup different deployment environments with Foundation (local, gcp, etc.) at both the project and global level. This allows users to customize their deployment environments and use a common one across multiple projects, or select specific environments per projects. Local configurations are stored in `/project_name/config`.

To set global environments, add `*.config.yaml` files to `~/.foundations/config`. If this diectory doesn't exist, you will need to create this directory first with:

```bash
mkdir ~/.foundations/config
```

To identify the different deployment environments setup on the machine:

```shellscript
$ foundations info --env
```

List all available environments and their paths. 

If you are within your project directory, this command lists the names and the paths of both your local environments as well as your global environments.

```bash
#Example output for info --env command when in project directory
global configs:
env_name    env_path
----------  ----------
local       /home/newHomeDir/.foundations/config/local.config.yaml
 
project configs:
env_name    env_path
----------  ------------------------------------------------------------
default     /home/newHomeDir/foundations/hana/config/default.config.yaml
local       /home/newHomeDir/foundations/hana/config/local.config.yaml
```
Otherwise, this command will only list the names and paths your global environments:  
```bash
#Example output for info --env command when not in project directory
global configs:
env_name env_path
---------- ----------
local       /home/newHomeDir/.foundations/config/local.config.yaml
```
