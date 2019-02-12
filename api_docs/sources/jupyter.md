
<h1>Jupyter Notebook start guide</h1>

*Foundations* itegates seemlessly with Jupyter notebook.

## Installation

1. To start, please follow the instructions in the [Start Guide](../start_guide/) to install the foundations library within a virtualenv on your machine. Don't forget to activate your virtualenv before you install foundations!

__Perform the following steps in your virtual env:__

2. Install Jupyter Notebook by running these commands in your terminal
```
pip install ipykernel
```
3. Install a new IPython kernel for running your Jupyter notebook. Note the python version of the notebook will match the python version of your virtualenv.
```
python -m ipykernel install --user --name=<kernel name>
```
4. Run the Jupyter notebook
```
jupyter notebook
```
5. Within the Jupyter notebook, switch the kernel to the <kernel-name> you just created by navigating to
  `Kernel > Change kernel > <kernel-name>`


6. If you're are planning to [run your project on a remote environment](../configs/), you may need to set environment variables in your notebook.

   For example, if you are deploying your job on Google Cloud Platform (GCP) you may need to set an environment variable pointing to a JSON keyfile.

   Run the below line in your notebook to set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`.
```
%env GOOGLE_APPLICATION_CREDENTIALS=/path/to/keyfile.json
```
   _Note: Environment variables need to be run in your notebook every time you refresh the kernel._


7. Now your notebook is setup for using Foundations and all its features for your new project! Check out our [step by step guide](../step_by_step_guide/) to get started with a basic example of what Foundations can do.
