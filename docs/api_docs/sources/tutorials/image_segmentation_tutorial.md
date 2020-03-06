#  Image Segmentation Tutorial

*Estimated time: 30 minutes*

Find code for this tutorial [here](https://github.com/dessa-public/Image-segmentation-tutorial).

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
  <iframe src="https://www.youtube.com/embed/TnMq0V_O1zs?start=146" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

## Introduction

This tutorial demonstrates how to make use of the features of Foundations Atlas. Note that any machine learning
job can be run in Atlas without modification. However, with minimal changes to the code we can take advantage of 
Atlas features that will enable us to launch many jobs and organize our model experiments more systematically.

This tutorial assumes that you have already installed Foundations Atlas. If you have not then you can download 
Atlas from [this link](https://www.atlas.dessa.com/) or use a cloud alternative as explained in the next section.

## Cloud option
Alternatively, if you have an AWS account, try using our <a target="_blank" href="https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/atlas-on-aws/">Atlas CE AMI</a> (publicly available Amazon Machine Image for Atlas).

The AMI will start by automatically installing the latest version of Atlas on a conda environment as well as starting the atlas server, and downloading this tutorial, (`cd atlas_tutorials/Image-segmentation-tutorial`) and you can directly skip to `Image Segmentation` section. The AMI supports both GPU and CPU instances.
## Local option
**Prerequisites**

1. Docker version >18.09 (Docker installation: <a target="_blank" href="https://docs.docker.com/docker-for-mac/install/"> Mac</a>
 | <a target="_blank" href="https://docs.docker.com/docker-for-windows/install/"> Windows</a>)
2. Python >3.6 (<a target="_blank" href="https://www.anaconda.com/distribution/">Anaconda installation</a>)
3. \>5GB of free machine storage
4. The atlas_ce_installer.py file (sign up and <a target="_blank" href="https://www.atlas.dessa.com/"> DOWNLOAD HERE </a>)


**Steps**

See <a target="_blank" href="https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/ce-quickstart-guide/">Atlas documentation</a>
  

<details>
  <summary>FAQ: How to upgrade an older version of Atlas?</summary>
<br>

1. Stop atlas server using <code>atlas-server stop</code> <br><br>
2. Remove docker images related to Atlas in your terminal with:
  <br><code>docker images | grep atlas-ce | awk '{print $3}' | xargs docker rmi -f</code><br><br>
3. Remove the environment where you installed the Atlas or pip uninstall the Atlas:
<br><code>conda env remove -n your_env_name</code><br><br>


</details>

## Image Segmentation

This tutorial demonstrates how to make use of the features of Foundations Atlas. Note that **any machine learning job can be run in Atlas without modification.** However, with minimal changes to the code we can take advantage of Atlas features that will enable us to:

* view artifacts such as plots and tensorboard logs, alongside model performance metrics
* launch many training jobs at once
* organize model experiments more systematically


## Data and Problem

The dataset that will be used for this tutorial is the <a target="_blank" href="https://www.robots.ox.ac.uk/~vgg/data/pets/">Oxford-IIIT Pet Dataset</a>, created by Parkhi *et al*. The dataset consists of images, their corresponding labels, and pixel-wise masks. The masks are basically labels for each pixel. Each pixel is given one of three categories :

* Class 1 : Pixel belonging to the pet.
* Class 2 : Pixel bordering the pet.
* Class 3 : None of the above/ Surrounding pixel.

Download the processed data [here](https://dl-shareable.s3.amazonaws.com/train_data.npz).

<img src='https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/data.png' width=70%>

## U-Net Model

The model being used here is a modified U-Net. A U-Net consists of an encoder (downsampler) and decoder (upsampler). In-order to learn robust features, and reduce the number of trainable parameters, a pretrained model can be used as the encoder. Thus, the encoder for this task will be a pretrained MobileNetV2 model, whose intermediate outputs will be used, and the decoder will be the upsample block already implemented in TensorFlow Examples in the [Pix2pix](https://github.com/tensorflow/examples/blob/master/tensorflow_examples/models/pix2pix/pix2pix.py) tutorial.
 
The reason to output three channels is because there are three possible labels for each pixel. Think of this as multi-classification where each pixel is being classified into three classes.

As mentioned, the encoder will be a pretrained MobileNetV2 model which is prepared and ready to use in [tf.keras.applications](https://www.tensorflow.org/versions/r2.0/api_docs/python/tf/keras/applications). The encoder consists of specific outputs from intermediate layers in the model. Note that the encoder will not be trained during the training process.

In the following sections, we will describe how to use this repository and train your own image-segmentation ML model in just a few steps.

Clone this repository by running:
```bash
git clone https://github.com/dessa-public/Image-segmentation-tutorial.git
```
and then type `cd Image-segmentation-tutorial` in the terminal to make this your current directory.

Paste the previously downloaded file named `train_data.npz` under the `data` directory of Image-segmentation-tutorial project.

## Start Atlas

Activate the conda environment in which Foundations Atlas is installed (by running `conda activte your_env` inside terminal). Then run `atlas-server start` 
in a new tab terminal. Validate that the GUI has been started by accessing it at <a target="_blank" href="http://localhost:5555/projects">http://localhost:5555/projects</a>.
(If using cloud, GUI should be accessible at <a target="_blank" href="http://localhost:5555/projects">http://<instance_IP>:5555/projects</a> insteal)

## Running a job

Activate the environment in which you have Foundations Atlas installed, then from inside the project directory (Image-segmentation-tutorial) run the following command:
```python
foundations submit scheduler . code/main.py
```
Notice that you didn't need to install any other packages to run your job because Foundations already takes care of it. This is ensured by the fact that you 
have a `requirements.txt` file in your main directory that specifies the python packages needed by your project. Foundations Atlas makes use of that file to 
install your requirements before executing your codebase.

If you take a look at Atlas dashboard, you can see basic information about the ran job such as start time, its status or its job ID.
You can also check the logs of your job by clicking the expand button on the right end of the job row of each job.

Congrats! Your run was scheduled by Foundations Atlas! It is important to notice that the initial codebase was written with no intention of using Atlas in 
mind. Despite using foundations to schedule the job, the codebase is not "aware" of the existence of Atlas.

Let's move on to explore the more advanced features of Atlas such as parameters and metrics tracking, models analysis, hyperparameter search and more.

## Atlas Features
The Atlas features include: 
1. Experiment reproducibility
2. Various jobs status monitoring (i.e. running, killed etc.) from GUI
3. Job metrics and hyperparameters analysis in the GUI
4. Saving and viewing of any artifacts such as images, audio or video from the GUI
5. Automatic job scheduling
6. Live logs for any running jobs and saved logs for finished or failed jobs are accessible from the GUI
7. Hyperparameter search
8. Tensorboard integration to analyze deep learning models
9. Running jobs in docker containers


## How to Enable Full Atlas Features

Inside the `code` directory, you are provided with the following python scripts:

* main.py: a main script which prepares data, trains an U-net model, then evaluates the model on the test set.

To enable Atlas features, we only to need to make a few changes. Let's start by importing foundations to the beginning of `main.py`, where we will make most 
of our changes:

```python
import foundations
```

## Logging Metrics and Parameters

When training machine learning models, it is always good practice to keep a record of the different architectures and parameters that were tried. Some 
example parameters are the number of layers, number of neurones per layer, dataset used or other parameters specific to the experiment.

To do that,
 Atlas enables
any job 
parameters to be logged in the GUI using `foundations.log_params()` which accepts key-value pairs.

Look for the comment:

```python
# TODO Add foundations.log_params(hyper_params)
```

replace this with:
```python
foundations.log_params(hyper_params)

```

Here, `hyper_params` is a dictionary in which keys are parameter names and values are parameter values.

In addition to keeping track of an experiment parameters, it is also good practice to record the outcome of such experiment, typically called metrics. Some 
example metrics can be Accuracy, Precision or other scores useful for the analysis of the problem.

In our case, the last line of `main.py` outputs the training and validation accuracy. After these statements, we will call the function `foundations
.log_metric()`.This function takes two arguments, a key and a value. After the function call has been added,  once a job successfully completes, logged metrics for each job will be visible from the Foundations GUI. Copy the following line and replace the print statement with it.

Look for the comment:

```python
# TODO Add foundations log_metrics here
```
replace this line with the lines below:
```python
foundations.log_metric('train_accuracy', float(train_acc))
foundations.log_metric('val_accuracy', float(val_acc))
```

## Saving Artifacts

We want to monitor the progress of our model while training by looking at the predicted masks for a given training image. With Atlas, we can save any artifact such as images, audio, video or any other files to the GUI with just one line.

It is worth noting that, in order to save artifact to Atlas dashboard, the artifact needs to be saved on disk first. The path of the file on disk is then 
used to log such artifacts to the GUI.

Look for the comment:
```python
# TODO Add foundations artifact i.e. foundations.save_artifact(f"sample_{name}.png", key=f"sample_{name}")
```
and replace it with:
```python
foundations.save_artifact(f"sample_{name}.png", key=f"sample_{name}")
```
Moreover, you can save the trained model checkpoint files as an artifact in GUI.

Look for the comment:
```python
# TODO Add foundations save_artifacts here to save the trained model
```
and replace it with:

```python
foundations.save_artifact('trained_model.h5', key='trained_model')
```
This will allow you to download the trained model corresponding to any experiment directly from GUI.

## TensorBoard Integration 


<a target="_blank" href="https://www.tensorflow.org/tensorboard/r1/summaries">TensorBoard</a> is a super powerful model visualization tool that makes 
the analysis of your training very easy. 

Luckily, Foundations Atlas has full TensorBoard integration. and only requires from the user to point to the folder where the user is saving his tensorboard 
files.

```python
# Add tensorboard dir for foundations here  i.e. foundations.set_tensorboard_logdir('tflogs')
```
Replace this line with
```python
foundations.set_tensorboard_logdir('tflogs')
```
to access TensorBoard directly from the Atlas GUI.


## Run Foundations Atlas

Congrats! Now you enabled full Atlas features in your code.

Now run the same command as you ran previously i.e. `foundations submit scheduler . code/main.py` from the `Image-segmentaion-tutorial` directory. 

This time, the job that we ran, holds a set of parameters used in the experiment, as well as the metrics representing the outcome of the experiment. More 
details about the job can be accessed via the expansion icon to the right of the row. The detail window includes job logs, as well as the artifacts saved 
along the experiment. It is also possible to add `tags` using the detail window to mark specific jobs.

On another level, one can also select a job (row) for the jobs table in the GUI and `send to tensorboard` to benefit from all the features avaiable in TB. It
 is usually a smart idea to do an in depth analysis of models to understand where they fail. Please note that jobs for which tensorboard files where tracked 
 by Atlas are marked with a tensorboard tag.

## Code Reproducibility

Atlas automatically provides you with the code reproducbility:

You can recover your code for any job at any time later in the future. In order to recover the code corresponding to any Foundations Atlas job_id, just execute 
```bash
foundations get job scheduler <job_id>
``` 
which will recover your experiment's bundle from the job store.

## (Optional) Build Docker Image

In previous runs, Foundations Atlas used to install the libraries inside `requirements.txt` everytime before executing the user's codebase. To avoid having 
such overhead at every new job, one might build a custom docker image that Foundations Atlas will use to run the experiments.

```bash
cd custom_docker_image
docker build . --tag image_seg:atlas
```
Since `customer_docker_image` folder already contains a `DockerFile` that would build a docker image that support both Foundations Atlas and the requirements
 of the project, you have created a docker image named `image_seg:atlas` on your local computer that 
conatins the 
python environment required to 
run this 
job.


### Running with the Built Docker Image: Configuration

In Atlas, it is possible to create a configuration job in your working directory that specifies some base information about all jobs you want to run. Such 
information can be the project name (defaults to directory name when non-existent), the level of log to receive, number of GPUs to use per job, or the docker
 image to use for every job.

Below is an example of configuration file that you can use for this project.

First, create a file named `job.config.yaml` inside `code` directory, and copy the text from below into the file. 

We will also make use of the docker image we have already built `image_seg:atlas`. 


```yaml
# Project config #
project_name: 'Image-segmentation-tutorial'
log_level: INFO

# Worker config #
# Additional definition for the worker can be found here: https://docker-py.readthedocs.io/en/stable/containers.html

num_gpus: 0

worker:
  image: image_seg:atlas # name of your customized images
  volumes:
    /local/path/to/folder/containing/data:
      bind: /data/
      mode: rw
```

Note: If you don't want to use the custom docker image, you can just comment out or just delete the whole `image` line inside `worker` section of this config file shown above.

Make sure to give right path of your data folder as shown below:

Under the `volumes` section, you will need to replace `/absolute/path/to/folder/containing/data` with your host absolute path of data folder so that your data 
volume is mounted inside the Foundations Atlas docker container. In order to obtain your absolute data path, you can `cd data` and then type `pwd` in the 
terminal

## Data Directory

Since we will mount our data folder from the host to the container, we need to change the data path appropriately inside our codebase.

```python
train_data = np.load('./data/train_data.npz', allow_pickle=True)
```
Replace the above block where the `train_data.npz` is loaded with the line below:
```python
train_data = np.load('/data/train_data.npz', allow_pickle=True)
```


## Run with full features of Foundations Atlas

Go inside the `code`directory and run the command below in your terminal (make sure you are in the foundations enviornment).
```python
foundations submit scheduler . main.py
```
This time we are running the `main.py` from inside the `code` directory. In this way, Foundations Atlas will only package the `code` folder and the `data` folder will get mounted directly inside Foundations Atlas docker container (as we specified inside the configuration file above). In this way, the data will not be a part of job package making it much faster and memory efficient.

At any point, to clear the queue of submitted jobs:
```python
foundations clear-queue scheduler
```

## How to Improve the Accuracy?
After running your most recent job, you can see that the validation accuracy is not very impressive. 
The predicted artifacts don't look similar to the true masks either. 

### Debugging with Tensorboard
Let's analyze the gradients using Tensorboard to understand what is happening with this sub par model. 
First click on the checkbox for your most recent job and press `Send to Tensorboard` button. 
This should open a new tab with Tensorboard up and running. 
Find the [histograms](http://localhost:5959/#histograms) tab. 

There you will see gradient plots such as below, where the first upsample layer has a range of gradients between 0.4 and -0.4:

Final upsample layer       |   Previous layers | ..  | First upsample layer| 
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/grad_4.png)  |  ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/grad_3.png) |  ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/grad_2.png) | ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/grad_0.png) 

As it is apparent from the plots, the gradients for the first upsample layer are small and centered around zero.
To prevent vanishing of gradients in the earlier layers, you can try modifying the code appropriately. 
Feel free to check the hints within the code! Alternatively the correct solution can be found below.

Validation accuracy | Validation loss
:-------------------------:|:-------------------------:
![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/validation_acc.png) | ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/validation_loss.png) 


### Solution
<details><summary>Click to See</summary>
<p>


Modern architectures often benefit from skip connections and appropriate activation functions to avoid the vanishing gradients problem.
Looking at the function `main.py/unet_model` reveals that the skip connections was not implemented, which prevents the gradient from finding an easy way back
 to the input layer (thus the gradient vanish). 
After the line `x = up(x)` add the below lines to fix this:
```
concat = tf.keras.layers.Concatenate()
x = concat([x, skip])
```

Another problem in the model is the usage of the sigmoid in the function `pix2pix.py/upsample` which is prone to saturation if the outputs pre-activation are
 of high absolute values. An easy, yet practical solution would be to replace the sigmoid activation functions with ReLu activations.
```
result.add(tf.keras.layers.Activation('sigmoid'))
```
Modify this line as below:
```
result.add(tf.keras.layers.ReLU())
```
Running another job with these changes results in a significantly higher accuracy, with below gradient plots, 
where the first upsample (`conv2d_transpose_4x4_to_8x8` under `grad_sequential`) layer has a range of gradients between 125 and -125 (300x greater now in magnitude!):

Final upsample layer       |   Previous layers | ..  | First upsample layer| 
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/fixed_grad_4.png)  |  ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/fixed_grad_3.png) |  ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/fixed_grad_2.png) |  ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/fixed_grad_0.png) 

Validation accuracy | Validation loss
:-------------------------:|:-------------------------:
![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/fixed_validation_acc.png) | ![](https://github.com/dessa-public/Image-segmentation-tutorial/raw/master/images/fixed_validation_loss.pngg)

</p>
</details>


## Running a Hyperparameter Search

Atlas makes running multiple experiments and tracking the results of a set of hyperparameters easy. Create a new file called 'hyperparameter_search.py' inside the `code` directory and paste in the following code:

```python
import os
import numpy as np
import foundations

NUM_JOBS = 10

def generate_params():

    hyper_params = {'batch_size': int(np.random.choice([8, 16, 32, 64])),
                    'epochs': int(np.random.choice([10, 20, 30])),
                    'learning_rate': np.random.choice([0.01, 0.001, 0.0001]),
                    'decoder_neurons': [np.random.randint(16, 512), np.random.randint(16, 512),
                                        np.random.randint(16, 512), np.random.randint(16, 512)],
                    }
    return hyper_params


for job_ in range(NUM_JOBS):
    print(f"packaging job {job_}")
    hyper_params = generate_params()
    foundations.submit(scheduler_config='scheduler', job_directory='.', command='main.py', params=hyper_params,
                       stream_job_logs=False)
```

This script samples hyperparameters uniformly from pre-defined ranges, then submits jobs using those hyperparameters. For a script that exerts more control 
over the hyperparameter sampling, check the end of the tutorial. The job execution code is still coming from main.py; i.e. each experiment is submitted to 
and run with the script.

In order to get this to work, a small modification needs to be made to main.py. In the code block where the hyperparameters are defined (indicated by the 
comment 'define hyperparameters'), we'll load the sampled hyperparameters instead of defining a fixed set of hyperparameters explicitly.

```python
# define hyperparameters: Replace hyper_params by foundations.load_parameters()
hyper_params = {'batch_size': 16,
                'epochs': 10,
                'learning_rate': 0.0001,
                'decoder
```
Replace the above block with the following:
```python
hyper_params = foundations.load_parameters()
```

Now, to run the hyperparameter search, from the `code` directory simply run:
```bash
python hyperparameter_search.py
```

By looking at the GUI, one might notice that some jobs are running, some others are maybe finished, while some others are still queued and waiting for 
resources to become available before starting to run.

It is however important to notice some key features that Atlas provides to make the hyperparameters search analysis easier:

- Sort parameters and metrics by value
- Filter out unwanted metrics/parameters to avoid information overflow in the GUI
- Parallel Coordinates Plot: A highly interactive plot that shows the correlation between parameters and metrics, or even the correlation between a set of 
metrics. It is possible to interact with the plot in real time to either select certain parameters/metrics, or to select specific jobs based on a range of 
metric values/parameter values. As such, one can easily detect the optimal parameters that contribute to the best metric values.
- Multi-job tensorboard comparison: It is very important to do an in-depth comparison of multiple different jobs using tensorboard to figure out the 
advantages and limitations of every architecture, as well as build an intuition about the required model type/complexity to solve the problem at hand.

## Congrats!
That's it! You've completed the Foundations Atlas Tutorial. Now, you know the bascis about this tool and you should be able to go to use it in your own project.

Do you have any thoughts or feedback for Foundations Atlas? Join the [Dessa Slack community](https://u12604448.ct.sendgrid.net/wf/click?upn=FWkFK8jQsWHHe3Zs0Gq5lTVfVJ15gKBcKJ8U8683-2FgbxDO0AKr58M46HvgnHq5gu7wxIxP578G4skYZ0QeDgMvlsnXObXuf729kfmWrTshGGl6TUN1-2FFyXqmyrD5ZoV-2FZRo0hnw3InKzQzFwqlF1quZt7VDueDH-2FEBH340YEI-2BzPVPIYVXfgn1PnGl8fkLCnbYCd3y-2FE9USkbXAlUUrS32M6lVOa8yh3Zx0NI6a4qqpVFMxksNDun1d3ARH2OSPbpz1vHZKPFnXOfLxXECu8PNhWW7f7-2FVoNinol6t-2BZkEIwfKAjbZI9cZRHYLkxGcq1fsHpXGYBb2nNHtUGC77Lo19RTjhUG7juCEF34X3kF4WvYGqy5xbhbLBL1VsCLH-2BckvPQvF-2Bungthb9Y9DVEIIY4DrphpWV2nxMH57ReudsB-2FoUEtHc18-2BSR84JprF1rfenfH4JeL2dr9DuunbkWvOph-2FkBza8U6YjdxtyfjjfJcoBacw-2B-2BmL6u6HWVn6M95UMOlfqzhF9cb-2FtspPAta5-2FN-2FXlygoZptG74-2B1qYgqeJKdfs8NNbZ21inPrj7an6r1nYNW4YC2xhFyLU2xQsBqtA-3D-3D_HUWHbgbBidglsEUmLbxZPG73zbI-2FXxUPQjCzMJWkdroEX4ThZ-2Ba-2FJdu8bhCG1wcvpbbfZo-2BiSSdhtu4tG6XMtkBL8Zae-2BGEwDN3szVNiE30Om1ynfKmNpOylsSRYgejDusVxPEBpP9-2FS7hlC9E8wo2TuFuHrlbl22LkB75K0wEtiJO0c2mViU1HaEmPEzBLCHXf0Y9-2BfRiS6YpAx89cMJwZ-2FMdDGn6VZ5J9E7sIA7uLAld9W8Xdng7daA-2B1UUesrCZrB378tYyV8RbFvAnAvAn08hSekPk-2B-2BE6Anb5HnHs8XDTwPMX7sPvViiOeXxCyHWzYDvS-2FTwddaZaPC2CL8lnQwdSWGGaDm1qQRQMv8W5CeeQbMj4Y4afLIpw6ujHEv9wrMcqEQ8WLNT0YmT8mXDJ-2FdsCQq8geKsHq4T8tWttr00sD8cyI7bWpNHnj05w2jgR0MVnuB3iWDUw-2F8P3yPB2-2BxfA34jXuxFn-2B30bf-2FOnkNcu-2B-2B0UeWmzxmjZyvxCXpjPvurewqGr-2Fpcx78JUfAHaFKyRorhoDV8yvd85XK-2BJ6vyGuwZ1wrEDBJTsE-2BGedJ)!


## References
1. https://www.tensorflow.org/tutorials/images/segmentation
1. https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/