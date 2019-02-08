<h1>Project creation</h1>

The best way to start using foundations is by creating a project using the foundations command line tool.

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

The `data` directory is intended as a place to put the data user's model requires as input.

The `project_code` directory contains two Python modules intended to be the files where user's solution main code resides. The module file named `model.py` is where Python functions that conform user's model should be defined. Each function there can be considered as a step (stage) towards building a model and can be imported later into the `driver.py` file to be invoked as a Foundations' stage. Of course, there could be more than just one source code file like `model.py`. The `driver.py` file is the main script that should be executed by the user and where stage creation and execution should happen.

The `post_processing` directory is where the user writes some code to interact with results that are available in the execution environment. By default a `results.py` script is created with some basic functionality to obtain metrics for all jobs.

At the root of the project's directory there is a `README.txt` file that explains the project structure just as this page does.
