# Start Guide

*Foundations* library can be used in any python machine learning development workflow.
It integrates easily with different stages(steps) of machine learning workflow irrespective of which machine-learning library.

To start with, first install the library and then follow examples guide to see how foundations can be used.

## Installation
Dependencies??? YAML and dill??
There are two ways to install foundations library:
[Wheel installation](https://github.com/DeepLearnI/foundations/STARTGUIDE.md/wheel-installation) or [Install from source](https://github.com/DeepLearnI/foundations/STARTGUIDE.md/install-from-source)

### Wheel Installation
The `.whl` files for python versions 2 and 3 are available per release on [release page](https://github.com/DeepLearnI/foundations/releases).
There are different assessts based on different job deployment strategies.
You only need `foundations-<version>-<python-version>-none-any.whl` file for initial foundations deployment.
Choose `whl` file as per python version installed the machine.

Run following command to install foundations
```
pip install -U <path-to-downloaded-whl-file>
```

### Install from source

Download sourcecode from github.
Specify Python version and run:
```
./build_dist.sh python<2_or_3>
```

### Examples guide
We have a [step by step guide](https://github.com/DeepLearnI/foundations/STEPBYSTEPGUIDE.md) on using Foundatoins with a very simple example.

We also have made it more clear on how to use different features of Foundations. We try to keep them up to date as we release new and update Foundations. You can [find them all here](https://github.com/DeepLearnI/foundations/examples).
