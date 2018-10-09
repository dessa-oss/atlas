# Start Guide

*Foundations* library can be used in any Python machine learning development workflow.
It integrates easily with different stages(steps) of the machine learning workflow irrespective of which machine learning library it's used with (Eg: Keras, Tensorflow).

To start with, first install the Foundations library and then follow examples guide to see how it can be used.

## Installation
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

## Environment and Dependencies

Foundations comes with a few dependencies that you'll see in [requirements.txt](https://github.com/DeepLearnI/foundations/blob/2018-10-19-rc/requirements.txt). The dependencies that get used when you run a job depend on your setup and deployment type.

If working with a remote deployment like GCP you'll need to know if the environment has the ability to download packages from the Internet. If yes, then specifying new dependencies in `requirements.txt` will allow the execution environment to download the necessary packages.

*If you run multiple jobs with different requirements, which one is used?*
Each time you run a job, the requirement.txt that is defined at run time is packaged and sent along with that job. Any changes to the `requirements.txt` file will only effect future jobs.

**Takeaway: if you expect a job to run with an external python package, you'll need to add it to your `requirements.txt` and the execution environment will need access to Internet to download.**

It's important to note: if you're looking to use a different version of a package than is installed by default on the execution environment (maybe XGBoost is installed on your GCP environment already), specifying a different version in your `requirements.txt` will **NOT** override the execution version. You'll need update the execution environment's version to do so.

Keep in mind that every time a job is run, a fresh python environment is created in the execution environment and all dependencies associated with the `requirements.txt` are installed. 

### Examples guide
We have a [step by step guide](STEPBYSTEPGUIDE.md) on using Foundations with a very simple example.

We also have made it more clear on how to use different features of Foundations. We try to keep them up to date as we release new and update Foundations. You can [find them all here](/examples).
