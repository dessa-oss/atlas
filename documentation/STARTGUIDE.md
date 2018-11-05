# Start Guide

*Foundations* library can be used in any Python machine learning development workflow.
It integrates easily with different stages(steps) of the machine learning workflow irrespective of which machine learning library it's used with (Eg: Keras, Tensorflow).

To start with, first install the Foundations library and then follow examples guide to see how it can be used.

## Installation

### Windows

You will need to install [git bash](https://git-scm.com/download/win) and [anaconda](https://conda.io/miniconda.html).
To run Foundations correctly, you will need to run all comands from an Anaconda prompt.

To install:

- Open an Anaconda prompt
- create a new conda environment by running `conda create --name foundations python=3.6`
- activate the environment by running `conda activate foundations`
- install foundations libraries via pip using the [Wheel installation](STARTGUIDE.md#wheel-installation)
- install additional dependencies via pip `pip install dill PyYAML pandas pysftp paramiko flask-restful Flask-Cors google-api-python-client google-auth-httplib2 google-cloud-storage futures promise`

See [running on Windows instructions](WINDOWS.md) for more details

### OSX/Linux

It's recommended that you use either `virtualenv` or `conda` to setup your Foundations environment.
Note: if using `virtualenv` make sure to create the environment outside the project directory as the directory will be compressed, and any extra dependencies will add to size and time for job running.

Dependencies: You will need to have `PyYAML` and `dill` installed on the machine before using Foundations.

There are two ways to install Foundations library:
[Wheel installation](STARTGUIDE.md#wheel-installation) or [Install from source](STARTGUIDE.md#install-from-source)

### Wheel Installation
The `.whl` files for Python versions 2 and 3 are available per release on our [release page](https://github.com/DeepLearnI/foundations/releases).
There are different assets based on different job deployment strategies.

You only need `foundations-<version>-<python-version>-none-any.whl` file for initial Foundations deployment.
Choose the appropriate `whl` file to match the Python version installed on your machine.

Run the following command to install Foundations:
```
python -m pip install -U <path-to-downloaded-whl-file>
```

### Install from source

Download Foundations' source code from Github.
In the root of the repo specify Python version and run:
```
./build_dist.sh
```

This builds a new `.whl` file of Foundations and installs it within your `conda` or `virtualenv` environment.

### Environment and Dependencies

Foundations comes with a few dependencies that you'll see in [requirements.txt](https://github.com/DeepLearnI/foundations/blob/master/requirements.txt). The dependencies that get used when you run a job depend on your setup and deployment type. To get to know the different deployment types better see our docs on [configurations](https://github.com/DeepLearnI/foundations/tree/master/examples/example_configs).

If working with a remote deployment like GCP you'll need to know if the environment has the ability to download packages from the Internet. If yes, then specifying new dependencies in `requirements.txt` will allow the execution environment to download the necessary packages.

If the environment doesn't have access to the Internet, expect that it will only use packages already installed by the system integrator. If additional packages need to be installed the job will not run. In the `stderr`, there will be a message notifying the user that the package could not be downloaded.

*If you run multiple jobs with different requirements, which one is used?*
If you have a `requirements.txt` in the same directory (root) as your model code, that requirements file will be packaged and sent along with the job to tell the execution environment what dependencies are needed. Any additional changes to `requirements.txt` will only effect future jobs.

**Takeaway: if you expect a job to run with an external python package, you'll need to add it to your `requirements.txt` and the execution environment will need access to Internet to download.**

It's important to note: if you're looking to use a different version of a package than is installed by default on the execution environment (maybe XGBoost is installed on your GCP environment already), specifying a different version in your `requirements.txt` will **NOT** override the execution version. You'll need update the execution environment's version to do so.

Keep in mind that every time a job is run, a fresh python environment is created in the execution environment and all dependencies associated with the `requirements.txt` are installed. This freshly created python environment also inherits any packages installed globally on the execution environment.

### Jupyter Notebook Setup
The full features of Foundations can also be used within a Jupyter notebook. Look at our [Jupyter Start Guide](JUPYTERSTARTGUIDE.md) to get started. 

### Examples guide
We have a [step by step guide](STEPBYSTEPGUIDE.md) on using Foundations with a very simple example.

We also have made it more clear on how to use different features of Foundations. We try to keep them up to date as we release new and update Foundations. You can [find them all here](/examples).
