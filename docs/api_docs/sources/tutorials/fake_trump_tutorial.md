# Fake vs. Real Trump Tweet Classifier Tutorial

*Estimated time: 30 minutes*

Find code for this tutorial [here](https://github.com/dessa-public/trump_tweet_classifier).

## Introduction

This tutorial demonstrates how to make use of the features of Foundations Atlas. Note that any machine learning
job can be run in Atlas without modification. However, with minimal changes to the code we can take advantage of 
Atlas features that will enable us to launch many jobs and organize our model experiments more systematically.

This tutorial assumes that you have already installed Foundations Atlas. If you have not then you can download 
Atlas from [this link](https://www.atlas.dessa.com/).

## Data
A csv file is included in the `code` folder which contains the tweets and labels.
You will need to download the pretrained word-embeddings from [here](https://fasttext.cc/docs/en/english-vectors.html). 
Download `wiki-news-300d-1M.vec.zip` and unzip it inside the `data` folder. The data folder should now have `wiki-news-300d-1M.vec` inside it. 


## The model
We train a deep 1D convolutional neural network that predicts the probability of a tweet being real or fake. 
In this repository, you can train this model by following the steps below.

## Requirements
1) Install Atlas from https://atlas.dessa.com
2) Install Docker from https://docs.docker.com/install/ and start the docker service locally on your computer
3) Install Anaconda (if not already installed)
4) Install `python >= 3.6.9` and `tensorflow==2.0rc` in a new environment via `requirements.txt`


## Why Atlas?

With Atlas, we're excited to bring you a machine learning platform 
shipping with a local scheduler and Python SDK which enables developers 
to manage hundreds of experiments while ensuring full reproducibility.
* Atlas allows you to quickly schedule Python code to be run on CPUs or GPUs.
* Atlas automatically creates the Python environment to run the job and discards it once the job is completed.
* Atlas allows the user to run and track many ML experiments. The Atlas GUI 
(running at https://localhost:5555) gives the user a comprehensive view 
of all the ML experiments in one place.


## Converting any code to run in Atlas
With only a few lines of code, you can convert your code to be Atlas-friendly. For reference, please see the `try/except` commands in `main.py` where we have introduced Atlas code to track ML experiments. 

Atlas spins up Docker containers to run the code. 
In order to provide the data to this Docker container, 
we need to mount the `data/` folder into the containers. 
In order to do so, open the `job.config.yaml` inside `code/` directory. Under the `volumes` section, replace the path (/Users/sachinrana/workspace/python_codes/trump_tweet_classifier/data/) with the absolute path of the data folder. By doing so, we are telling foundations to mount this data/ folder inside the docker container from which the code will read the required files. 

## Running the code 
`cd` into the `code` directory in order to run `main.py`. You may run the job with or without Atlas. Use these commands to run the code.


| Run Job           | Terminal command                |   Purpose              |   
|----------------|--------------------------|-----------------------------------|
|      Without Atlas     | `python main.py`           | To run code normally               |                          
| Only one job with Atlas | foundations submit scheduler . main.py       | To run any python code with foundations                 |
|      Run multiple ML experiments with Atlas    | python submit_jobs.py                   | To track multiple experiments and find the best ML model                |


## Baseline model
Around line 68 in `main.py`, we have included a flag `USE_BASELINE_PARAMS = False` 
so you can run experiments with random hyperparameters. To run just the baseline model, set this flag to be `True`.

The baseline validation accuracy is ~75%. With some experimentation, this accuracy can be improved.

Below are some screenshots of running ML experiments with Atlas.

## Run a single job with foundations
![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/single_deploy_cli.png)

Once the job is deployed from the terminal, it can be viewed in the Atlas GUI by going to your internet browser at https://localhost:5555.

![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/single_job_running_gui.png)


## Launch multiple experiments with Atlas
![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/submit_jobs_cli.png)
![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/multiple_experiments_gui.png)

## Saving artifacts with Atlas

Artifacts are objects such as images, generated audio, confusion matrices, or input distribution statistics
which need to be tracked for reproducibility. 
These artifacts are accessible from the GUI.

The GUI shows the run status of each experiment, along with their performance. 
In order to view the performance plots, click on the square box at the end of a row. 
You should see the Artifacts window pop up, where you can see the `performance_plots.png` and `saved_model.h5`.

Artifacts can be used to save the trained model to be used for production or further analysis. 
From the artifact viewer, you can download the trained model file, `saved_model.h5`

![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/artifacts_viewer.png)

To see the performance plots while training a model, click on `performance_plots.png`.

![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/view_artifact_1.png)
![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/view_artifact_2.png)



Clicking on `Project Overview` will bring up a plot of model metrics for each experiment that was run using Atlas.

![](https://github.com/dessa-public/trump_tweet_classifier/raw/master/code/images/metrics_tracking_per_experiment.png)

That's it! Try running some experiments using Atlas 
and [let us know](https://twitter.com/dessa) if you have feedback, 
questions or suggestions. Happy experimenting!








