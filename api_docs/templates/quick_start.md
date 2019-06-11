<h1>Quick-Start Guide</h1>

Welcome to the Foundations quick-start guide! The following instructions should help you get setup with Foundations as quick as possible and ready to run your first job on your local machine. For more information on any of the steps, please refer to the full [installation](../start_guide/) guide.

#Installation Prerequisites

Before getting started, you will need Python 3.x installed on your machine. If you plan to use Tensorflow, we recommend using versions <= `Python 3.6` as it does not support versions greater at the moment. 

<h2>macOS/Linux</h2>

To run Foundations, you will need [Docker](https://docs.docker.com/docker-for-mac/install/) ( Version >= 18.09 )   

We also recommend using [Anaconda](https://www.anaconda.com/distribution/#macos) ( Python 3.x version ) to setup a virtual environment where all packages can be installed and maintained with ease.

<h2>Windows</h2>

Before getting started with Foundations, you will need the following tools on your machine:  

* [Anaconda](https://conda.io/miniconda.html) ( Python 3.x version )  
* [Docker](https://docs.docker.com/docker-for-windows/install/) ( Version >= 18.09 )  
* [Git Bash](https://git-scm.com/download/win)  

To run Foundations correctly, you will need to setup the environment from an Anaconda prompt, then use Git Bash to setup the GUI (optional) and deploy jobs.

## 0. Setup Access to Dessa Private Repository
To setup Foundations, you will first need access to the Dessa private pip and docker repositories. Please reach out to the Dessa team for necessary credentials.

For Pip access, you will need a `pip.conf` or `pip.ini` with credentials to Dessa's private pip repository. This file should be placed in `~/.config/pip/pip.conf` (macOS/Linux) or ``~/AppData/Roaming/pip/pip.ini` (Windows).

For Docker access, this can be setup with the command: `docker login`.

## 1. Setup Conda Environment
To setup Foundations, we recommend establishing a virtual environment where all packages can be installed and maintained with ease. They also isolate the dependencies of different individual projects, avoiding Python version conflicts and prevent permission issues for non-administrator users.

For this tutorial, we will be using ```Anaconda``` to setup Foundations; however, other package managers such as `venv` or `pyenv` can be used as well. To create a new python environment, run the following commands in either terminal (macOS/Linux) or in a new Anaconda prompt (Windows):
```bash
conda create --name foundations_env python=3.6
```

*Note:* We use Python 3.6 since Tensorflow only supports up to 3.6 at the moment.

Next, activate the environment by running:
```bash
conda activate foundations_env
```

To deactivate the environment you are using with Foundations, you can run:
```bash
conda deactivate
```

For additional information on managing Conda envionments, please refer to the documentation [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

## 2. Install Foundations
For Windows users, please open a new git bash prompt, we will be using git bash as our primary interface for all commands for the rest of the tutorial.

To install the latest version of Foundations, run:

```bash
pip install dessa-foundations
```

To check that Foundations is installed, you can verify that the Foundations CLI tool is available with:
```bash
foundations
```

For more information about getting access, please reach out to the Dessa Integrations team.

## 3. Create a new Foundations Project

To create a new Foundations Project, run the following command:
```bash
foundations init <project_name>
```

This will create a basic folder structure with a local ```config.yaml``` file as well as folders for your model and deployment code. More information on the CLI and ```init``` can be found [here](../project_creation/) .

## 4. Setting up Redis and GUI (local deployment only)

Foundations uses [Redis](https://redis.io/) as a quick and efficient way to store data for experiments. This, as well as the Foundations GUI for visualizing experiments, can be setup with a Foundations CLI command:

```bash
foundations setup
```

Once completed, you will be able to visit your running GUI at `https://localhost:6443`.

**Note: Other instances of Redis on the same machine may interfere with the setup through Docker.** For more information please reference the Redis [guide](../start_guide/#redis-setup). In addition, you will need access to the private docker repository containing the Foundation GUI images. 

## 5. (OPTIONAL) Starting Jupyter Notebook

Foundations integates seemlessly with Jupyter Notebook for users who prefer to use Jupyter to develop machine learning models. However, this is not a mandatory requirement with Foundations, as you can also deploy models natively. 

To use Jupyter, first create a new kernel by navigating to your project directory and running the following:

```bash
pip install ipykernel
python -m ipykernel install --user --name=<kernel name>

#Start Jupyter Notebook which is available at http://localhost:8888 by default
jupyter notebook
```
Then switch the Kernel to the one you just created by navigating to:  
```Kernel > Change kernel > <kernel-name>```

## 6. Starting Your First Project

That's it! Foundations should now be setup and ready to use on your local machine. For a step-by-step guide on your first project, check out our [step-by-step guide](../step_by_step_guide/).