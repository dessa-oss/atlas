# Start Guide

*Foundations* library can be used in any Python machine learning development workflow.
It integrates easily with different stages(steps) of the machine learning workflow irrespective of which machine learning library it's used with (Eg: Keras, Tensorflow).

To start with, first install the Foundations library and then follow examples guide to see how it can be used.

## Installation
It's recommended that you use either `virtualenv` or `conda` to setup your Foundations environment.
Note: if using `virtualenv` make sure to create the environment outside the project directory as the directory will be compressed, and any extra dependencies will add to size and time for job running.

Dependencies: You will need to have `PyYAML` and `dill` installed on the machine before using Foundations.

There are two ways to install Foundations library:
[Wheel installation](https://github.com/DeepLearnI/foundations/blob/master/documentation/STARTGUIDE.md#wheel-installation) or [Install from source](https://github.com/DeepLearnI/foundations/blob/master/documentation/STARTGUIDE.md#install-from-source)

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
./build_dist.sh python<2_or_3>
```

This builds a new `.whl` file of Foundations and installs it within your `conda` or `virtualenv` environment.

### Examples guide
We have a [step by step guide](https://github.com/DeepLearnI/foundations/blob/master/documentation/STEPBYSTEPGUIDE.md) on using Foundations with a very simple example.

We also have made it more clear on how to use different features of Foundations. We try to keep them up to date as we release new and update Foundations. You can [find them all here](https://github.com/DeepLearnI/foundations/tree/master//examples).
