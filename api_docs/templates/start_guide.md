<h1>Installation Guide</h1>

*Foundations* only support Python 3 and above versions. 

First, lets install the Foundations library and then follow a [step-by-step](../step_by_step
_guide/) guide to see how it can be used.

##OSX/Linux

It's recommended that you use either [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) or [conda](https://conda.io/projects/conda/en/latest/user-guide/index.html) to setup your Foundations environment.

Note: if using `virtualenv` make sure to create the environment outside the project directory as the directory will be compressed, and any extra dependencies will add to size and time for job running.

There are two ways to install Foundations library, either by Wheel installation or from the source directly.

<h3>Wheel Installation</h3>
The `.whl` files for Python 3.X are available and will be provided by the Dessa team.
There are different assets based on different job deployment strategies.

You only need `foundations-<version>-py3-none-any.whl` file for initial Foundations deployment.

Run the following command to install Foundations:
```
python -m pip install -U <path-to-downloaded-whl-file>
```

<h3>Install from source</h3>

Download Foundations' source code from Github via:
```bash
git clone https://github.com/DeepLearnI/foundations
```
In the root of the repo specify Python version and run:
```bash 
./build_dist.sh
```
This will build a new `.whl` file of Foundations and install it within your `conda` or `virtualenv` environment.

## Environment and Dependencies

When installing from the source code, Foundations comes with a few dependencies that you'll see in `requirements.txt`. These are used to specify which packages are required for Foundations to run correctly. 

In addition, users can also specify specifc `requirements.txt` at the job level. By creating a `requirements.txt` file in the same directory as your driver code, the dependencies defined in the file will be  used when you run a job depending on your setup and deployment type. To get to know the different deployment types better see our docs on [configurations](../configs/).

If working with a remote deployment like GCP you'll need to know if the environment has the ability to download packages from the Internet. If yes, then specifying new dependencies in the job-level `requirements.txt` will allow the execution environment to download the necessary packages.

If the environment doesn't have access to the Internet, expect that it will only use packages already installed by the system integrator. If additional packages need to be installed the job will not run. In the `stderr`, there will be a message notifying the user that the package could not be downloaded.

*If you run multiple jobs with different requirements, which one is used?*
If you have a `requirements.txt` in the same directory (root) as your job deployment code, that requirements file will be packaged and sent along with the job to tell the execution environment what dependencies are needed. If using the [Foundations CLI](../project_creation/) `init` command to setup a project directory, this would be the project_code directory. Any additional changes to `requirements.txt` will only effect future jobs.

**Takeaway: if you expect a job to run with an external python package, you'll need to add it to your `requirements.txt` and the execution environment will need access to Internet to download.**

It's important to note: if you're looking to use a different version of a package than is installed by default on the execution environment (maybe XGBoost is installed on your GCP environment already), specifying a different version in your `requirements.txt` will **NOT** override the execution version. You'll need update the execution environment's version to do so.

Keep in mind that every time a job is run, a fresh python environment is created in the execution environment and all dependencies associated with the `requirements.txt` are installed. This freshly created python environment also inherits any packages installed globally on the execution environment.

## Redis Setup

The Foundations uses Redis as a quick and efficient way to store data for experiments. In order to run Foundations with local deployment, you'll first need to install Redis. Note: The following steps will apply for local job deployments only, the Dessa team will setup the Redis for any remote deployments (GCP, AWS, etc.)

Steps to running Redis:

- download and [install Docker](https://www.docker.com/get-started) if not already installed
- download redis with `docker pull redis`
- start redis with `docker run -d -p 6379:6379 redis`

The `-d` option will allows us to run in detached mode, so you don't have to keep your shell open.

The `-p` option allows us to publish a container's port to the host. In this case this means we've told docker that port 6379 inside the container should map to port 6379 of our machine.

Now that redis is running, when you run a job locally it'll get picked and and handled by Redis. Additionally anytime you read results, Foundations will access the Redis store.

If you want to stop the Redis container, run `docker ps`, get the container's ID, and then run `docker stop <container_id>`.

**Note: Other instances of Redis (such as via Homebrew) running on the same machine may interfere with this setup.** We recommend stopping or disabling other instances and running Redis through Docker.  
  
To stop Homebrew Redis instances:   
  
<span>1. </span>In bash or terminal, check the process status:
```bash
ps aux | grep redis
```

Then kill the process with:  
```bash
kill <process id>
```  
  
<span>2. </span>Uninstall Redis with:  
```bash
brew uninstall redis
```

## Jupyter Notebook Setup
*Foundations* itegates seemlessly with Jupyter notebook.

<h3>Installation</h3>

__Perform the following steps in your virtual env:__

<span>1.</span> Install Jupyter Notebook by running these commands in your terminal
```
pip install ipykernel
```
<span>2.</span> Install a new IPython kernel for running your Jupyter notebook. Note the python version of the notebook will match the python version of your virtualenv.
```bash
python -m ipykernel install --user --name=<kernel name>
```
<span>3.</span> Run the Jupyter notebook
```
jupyter notebook
```
<span>4.</span> Within the Jupyter notebook, switch the kernel to the <kernel-name> you just created by navigating to
`Kernel > Change kernel > <kernel-name>`

<span>5.</span> If you're are planning to [run your project on a remote environment](../configs/), you may need to set environment variables in your notebook.

For example, if you are deploying your job on Google Cloud Platform (GCP) you may need to set an environment variable pointing to a JSON keyfile.

Run the below line in your notebook to set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`.
```
%env GOOGLE_APPLICATION_CREDENTIALS=/path/to/keyfile.json
```
_Note: Environment variables need to be run in your notebook every time you refresh the kernel._

<span>6.</span> Now your notebook is setup for using Foundations and all its features for your new project! Check out our [step by step guide](../step_by_step_guide/) to get started with a basic example of what Foundations can do.

## Installing and Running the GUI
Foundations provides a user interface with which one can view all information about jobs, including status (e.g. queued, running, completed) as well as logged metrics and start time.  As for how to to install and use it, have a look at the [GUI guide](../gui/).
