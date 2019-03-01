<h1>Quick-Start Guide</h1>

Welcome to the Foundations quick-start guide! The following instructions should help you get setup with Foundations as quick as possible and ready to run your first job on your local machine. For more information on any of the steps, please refer to the full [installation](../start_guide/) guide.

#OSX/Linux

Before getting started, you will need Python 3 installed on your machine. If you plan to use Tensorflow, we recommend using versions <= `Python 3.6` as it does not support versions greater at the moment:  

As well as the following tools:   
[Docker](https://docs.docker.com/docker-for-mac/install/) ( Version >= 18.09 )   
[Jupyter Notebook](https://jupyter.org/install)

## 1. Setup Virtual Environment
To first setup Foundations, we recommend establishing a virtual environment where all packages can be installed and maintained with ease. For this tutorial, we will be using ```virtualenv``` to setup Foundations; however, other package managers such as Conda can be used as well. This can be installed using:
```bash
pip install virtualenv
```

To create a python environment, run the following commands:
```bash
virtualenv -p python3.6 venv
source venv/bin/activate
```

Note: We use Python 3.6 since Tensorflow only supports up to 3.6 at the moment

## 2. Install Foundations via Source
For users who do not have access to github, Foundations can also be installed by Wheel installation. More information on installing Foundations can be found [here](../start_guide/)

Download the Foundations' source code from Github:
```bash
git clone https://github.com/DeepLearnI/foundations
```
Navigate to the main root directory of the repository and build packages:
```bash
cd foundations
./build_dist.sh
```

The ```build_dist``` script will build a new ```.whl``` file of Foundations and installs it within your virtualenv environment.

Next, install the dependencies located in ```requirements.txt```. These are packages that Foundations' needs to run. More information can be found [here](../start_guide/#environment-and-dependencies/).

```bash
python -m pip install -r requirements.txt
```

## 3. Create a new Foundations Project

To create a new Foundations Project, run the following command:
```bash
foundations init <project_name>
```

This will create a basic folder structure with a local ```config.yaml``` file as well as folders for your model and deployment code. More information on the CLI and ```init``` can be found [here](../project_creation/) .

## 4. Setting up Redis (local deployment only)

The [Redis](../start_guide/#redis-setup) acts as a quick and efficient way to store data for experiments. In order to run Foundations with local deployment, you'll first need to install Redis. 

Navigate to the root directory of the repository and run:

```bash
docker pull redis
docker run -d -p 6379:6379 redis
```

You can verify that the redis is up and running with where you should see a container called `redis` using port 6379:

```bash
docker ps
```

**Note: Other instances of Redis on the same machine may interfere with the setup through Docker.** For more information please reference the Redis [guide](../start_guide/#redis-setup)

## 5. (OPTIONAL) Setting up GUI locally

The Foundations [GUI](../gui/) provides a user interface where a user can view all information about jobs, simplifying experiment management. This is not mandatory to use foundations as experiments can still be retrieved through the SDK.

To setup the GUI locally, first please ensure the Redis is setup as specified above. Then, navigate to the root directory of the Foundations repository and run:  
```bash
./build_gui.sh
```
The ```build_gui.sh``` script will build and tag the docker images for the GUI and REST API, which will communicate with the Redis.

Next, you will need to set the location of your Redis installation by setting the ```REDIS_URL``` environment variable. This will need to be set to the IP address of your local machine, which can be found **[here](https://www.whatismybrowser.com/detect/what-is-my-local-ip-address)  .**


```bash
export REDIS_URL=redis://<local ip of machine>
```

For example, if your machine's IP address is ```22.23.43.22```, you will need to run the following:
```bash
export REDIS_URL=redis://22.23.43.22
```

You can verify that ```REDIS_URL``` is setup correctly by typing ```echo $REDIS_URL``` . Now you're ready to start the GUI! Run the following command:

```bash
./foundations_gui.sh start ui
```  
You will then be able to visit your running gui at ```https://localhost:6443```

## 6. (OPTIONAL) Starting Jupyter Notebook

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

## 7. Starting Your First Project

That's it! Foundations should now be setup and ready to use on your local machine. For a step-by-step guide on your first project, check out our [step-by-step guide](../step_by_step_guide/).

#Windows

Before getting started, you will need [git bash](https://git-scm.com/download/win) and [anaconda](https://conda.io/miniconda.html). To run Foundations correctly, you will need to setup the environment from an Anaconda prompt, then use Git Bash to setup the GUI (optional) and deploy jobs.

You will also need the following tools:   
[Docker](https://docs.docker.com/docker-for-windows/install/) ( Version >= 18.09 ) 

## 1. Setup Conda Environment

Create a new Conda environment which we will install the Foundation packages into. To do this, open tbe Anaconda Navigator and open an Anaconda prompt. Then, create a new environment by running:
```bash
conda create --name found-env python=3.6
```

Next, activate the environment by running:
```bash
conda activate found-env
```

Finally, we need to install a few packages with pip:
```bash
pip install dill PyYAML pandas pysftp paramiko flask-restful Flask-Cors google-api-python-client google-auth-httplib2 google-cloud-storage futures promise
```

## 2. Install Foundations via Wheel

The `.whl` files for Python 3 are available and will be provided by the Dessa team. In the Anaconda prompt, enter:

```bash
python -m pip install -U <absolute-path-to-downloaded-whl-file>
```
Or if you are already in the same directory:
```bash
python -m pip install -U <downloaded-whl-filename>
```

You can confirm the Wheel files have been properly installed by accessing the [Foundations CLI](../project_creation/) via:
```
python -m foundations
```
which should return a list of available options.  

From here, please open a new git bash instance and activate the conda environment via:
```bash
source activate found-env
```
**Note: For the rest of this tutorial we will be using git bash as our primary interface for all commands.**

## 3. Create a new Foundations Project

To create a new Foundations Project, run the following command:
```bash
python -m foundations init <project_name>
```

This will create a basic folder structure with a local `default.local.yaml` config file as well as folders for your model and deployment code. More information on the CLI and `init` can be found [here](../project_creation/) .

In order to deploy jobs locally, you may also need to update the `shell_command` path in the generated config file. This allows Foundations to understand how to deploy shell scripts which are required for running jobs by pointing to the location of git bash. The recommended value for this is `C:\\Program Files\\Git\\bin\\bash.exe`,
but if you changed this path during installation, you will have to change this value respectively. More information can be found [here](../windows/#local-deployment)

## 4. Setting up Redis (local deployment only)

The [Redis](../start_guide/#redis-setup) acts as a quick and efficient way to store data for experiments. In order to run Foundations with local deployment, you'll first need to install Redis:

```bash
docker pull redis
docker run -d -p 6379:6379 redis
```

You can verify that the redis is up and running with where you should see a container called `redis` using port 6379:

```bash
docker ps
```

**Note: Other instances of Redis on the same machine may interfere with the setup through Docker.** For more information please reference the Redis [guide](../start_guide/#redis-setup)

## 5. (OPTIONAL) Setting up GUI locally

The Foundations [GUI](../gui/) provides a user interface where a user can view all information about jobs, simplifying experiment management. This is not mandatory to use foundations as experiments can still be retrieved through the SDK.

To setup the GUI locally you will need the Foundations source code repository from github. First, open a new git bash instance and before cloning the repository and enter:
```bash
git config --global core.autocrlf false
```

This will ensure that git clones the repository and properly handle line endings so that the git bash can run shell scripts properly. Next (still in the *git bash*), download the repository, navigate to the root directory of the repo, and run the `build_gui.sh` script which will build and tag the docker images for the GUI and REST API, which will communicate with the Redis:
```bash
git clone https://github.com/DeepLearnI/foundations
cd foundations
./build_gui.sh
```

Next, you will need to set the location of your Redis installation by setting the `REDIS_URL` environment variable. This will need to be set to the IP address of your local machine.

```bash
export REDIS_URL=redis://<local ip of machine>
```

For example, if your machine's IP address is ```22.23.43.22```, you will need to run the following:
```bash
export REDIS_URL=redis://22.23.43.22
```

You can find your local IP [here](https://www.whatismybrowser.com/detect/what-is-my-local-ip-address) .

You can verify that ```REDIS_URL``` is setup correctly by typing ```echo $REDIS_URL``` . Now you're ready to start the GUI! Run the following:

```bash
./foundations_gui.sh start ui
```  
You will then be able to visit your running gui at ```https://localhost:6443```

## 6. (OPTIONAL) Starting Jupyter Notebook

Foundations integates seemlessly with Jupyter Notebook for users who prefer to use Jupyter to develop machine learning models. However, this is not a mandatory requirement with Foundations, as you can also deploy models natively.  

To use Jupyter, navigate to your project directory and running the following:

```bash
#Start Jupyter Notebook which is available at http://localhost:8888 by default
jupyter notebook
```
If you encounter issues with importing the Foundations library, try creating a new Kernel first via:

```bash
pip install ipykernel
python -m ipykernel install --user --name=<kernel name>
jupyter notebook
```
Then switch the Kernal to the one you just created by navigating to:  
```Kernel > Change kernel > <kernel-name>```

## 7. Starting Your First Project

That's it! Foundations should now be setup and ready to use on your local machine. For a step-by-step guide on your first project, check out our [step-by-step guide](../step_by_step_guide/).