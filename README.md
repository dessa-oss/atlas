[![Build Status](https://jenkins.shehanigans.net/buildStatus/icon?job=atlas%2Fmaster&subject=build%20${buildId}%20took%20${duration})](https://jenkins.shehanigans.net/job/atlas/job/master/)
![Platform Support](https://img.shields.io/badge/Platforms-osx%20%7C%20linux%20%7C%20windows-lightgrey "platform")
![Python Support](https://img.shields.io/badge/Python-%3E3.6-blue "python")
![Downloads](https://img.shields.io/badge/Downloads-2000+-blue "downloads")

<p align="center">
  <img width="20%" src="dessa-square-logo.png">
</p>

---

# Atlas: Self-Hosted Machine Learning Platform
Atlas is a flexible Machine Learning platform that consists of a Python SDK, CLI, GUI & Scheduler to help Machine Learning Engineering teams dramatically reduce the model development time & reduce effort in managing infrastructure.

## Features
Here are few of the high-level features:
1. _Self-hosted_: run Atlas on a single node e.g. your latop, or multi-node cluster e.g. on-premise servers or cloud clusters (AWS/GCP/etc.)
2. _Job scheduling_: Collaborate with your team by scheduling and running concurrent ML jobs remotely on your cluster & fully utilize your system resources.
3. _Flexibility_: Multiple GPU jobs? CPU jobs? need to use custom libraries or docker images? No problem - Atlas tries to be unopionated where possible, so you can run jobs how you like.
4. _Experiment managment & tracking_: Tag experiments and easily track hyperparameters, metrics, and artifacts such as images, GIFs, and audio clips in a web-based GUI to track the performance of your models.
5. _Reproducibility_: Every job run is recorded and tracked using a job ID so you can reproduce and share any experiment.
6. _Easy to use SDK_: Atlas's easy to use SDK allows you to run jobs programatically allowing you to do multiple hyperparameter optimization runs programatically
7. _Built in [Tensorboard](https://github.com/tensorflow/tensorboard) integration_: We ❤️ Tensorflow - compare multiple Tensorboard-compaitable job runs directly through the Atlas GUI.
8. _Works well with others_: run any Python code with any frameworks.

<p align="left">
  <img width="25%" src="atlas-logo.gif">
</p>

## Installation 
TODO

## Documentation
Official documentation for Atlas can be found at https://www.docs.atlas.dessa.com/

## System Overview
TODO

## Community 
For help or questions about Atlas see the [docs](https://www.docs.atlas.dessa.com/), [Stack Overflow](https://stackoverflow.com/questions/tagged/foundations-atlas), or join the [Dessa Slack](https://join.slack.com/t/dessa-community/shared_invite/enQtNzY5ODkxOTc3OTkwLTk4MTg5NmNkOTQ5OWVjNjk2YzY0OWJlNDkwNDlhY2NmNTQzNmRmYjkxNzc2N2JiOTYxZGVkMmFiMjRhYThiYzM).

To report a bug, file a documentation issue, or submit a feature request, please open a GitHub issue.

## Development Status
Atlas has evolved very rapidly and has gone though many iterations in Dessa's history. 

The latest version is in BETA. 

## Contributing
We ❤️ contributors and would love to work with you. When you are ready, just follow the steps below in order to set up a development environment.

1. You will need to have `docker`, `yarn`, and the `envsubst` command line tool on your machine in order spin up a local development environment.    
  `brew install docker`  
  `brew install yarn`  
  `brew install gettext`  
  If you are on a linux machine then replace `brew install` with the equivalent command for your distributions package manager.  

2. Clone this repository and enter the new directory  
  `git clone git@github.com:DeepLearnI/atlas.git && cd atlas`  

3. Create and activate a brand new virtual environment with Python 3.7 then install the requirements. Some examples below.
   Conda:  
    `conda create --name foundations python=3.7 && conda activate foundations`  
    `pip install -r requirements_dev.txt`  
   Pipenv:  
    `pipenv --python 3.7 && pipenv shell`  
    `pipenv install`  
    `pipenv install -r requirements_dev.txt --dev --pre --skip-lock`  
  Venv:  
    `python3 -m venv . && source bin/activate`  
    `pip install -r requirements_dev.txt`  

4. Add the packages that make up Atlas to your python path and set some environemnt variables by sourcing the `activate_dev_env.sh` file.  
   `. activate_dev_env.sh`  

5. Generate the required configuration files.  
   `make devenv-configure`  

6. Launch Atlas in development mode. This may take a while to pull some required docker images.  
   `make devenv-start`  

7. You can now create a sample project by running the following command.  
  `python -m foundations init my-project`  

8. Change into the newly created project directory and execute the following command to submit your first job. This can take a while the first time as one more image may need to be pulled.  
  `python -m foundations submit scheduler . main.py`  
   
9. Navigate to `localhost:3000` and verify that your newly created project exists on the frontend. Click on the project and verify that your job executed successfully.

10. Congrats! You are ready to go.


## License
```
Copyright 2015-2020 Square, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```