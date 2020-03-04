# Atlas on GCP

Being able to run Atlas on GCP means access to GPUs, and more importantly faster model results. In this tutorial we'll walk through setting up and running jobs on GCP with Atlas, as well as running experiments from VSCode.

Requirements

* GCP account
* gcloud CLI tool installed (<a target="_blank" href="https://cloud.google.com/sdk/downloads/">download</a>)


### Step 1: Setting up Deep Learning VM 

First let's go to the GCP developer console, sign in, and then we'll create a new instance using the: <a target="_blank" href="https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning">GCP Deep Learning VM</a>. It will prompt us to select a project, and select the appropriate project for the instance to run under.

This VM will give us access to an instance with a GPU, as well as built-in libraries like Docker, and Tensorflow.

Click the **"Launch on compute engine"** button to start setup.

![create instance](assets/images/gcp-create-instance.png)

### Step 2: Deployment settings

There's a few updates we'll need to make to the instance before we deploy it. The below settings are optimal for trying out Atlas, but if you're starting a bigger project, feel free to add more compute, memory, or disk space.

* Set a deployment name
* Zone: select a zone that with K80 GPUs available (for our use, we'll select **us-east1-c**)
* Machine Type: the default of 2 vCPUs, with 13 GB of memory is fine
* GPUs: select 1 NVIDIA Tesla K80 GPU
* Framework: nothing to change here
* GPU: check the **"Install NVIDIA GPU driver automatically on first startup"** box to make sure we have access to the GPUs
* Boot disk: can keep as "Standard Persistent Disk"
* Boot disk size: we'll bump this up to 150GB
* Networking: nothing to change

!!! note
    K80 GPUs are not the most powerful, but for most simple uses of GPUs it should suffice. If you're doing data intensive work you may want to select an instance with a P100 GPU

We should now be good to spin up the instance, just click the **Deploy** button.

It will take about 5 minutes for the instance to initialize.

### Step 3: Setup Atlas

Use the provided gcloud CLI command to SSH into the instance. It should look similar to:

![SSH into instance](assets/images/gcp-ssh-instance.png)

We can take this command and run it in our terminal to SSH into the instance. Make sure you have the gcloud CLI tool setup prior to doing this.

Once inside the instance we now need to install Atlas. 

We've put together a script that does a lot of the leg work (create environments and installing Atlas).

1. Save the following script as a file **install_atlas.sh**
```
#!/bin/bash

wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh -O ~/miniconda.sh
bash $HOME/miniconda.sh -b -p $HOME/miniconda
eval "$($(pwd)/miniconda/bin/conda shell.bash hook)"
conda init
source ~/.bashrc

# create conda env for atlas installation if not already exists
if [[ $(conda env list | grep atlas_ce_env | awk '{print $1}') != 'atlas_ce_env' ]]; then
   conda update -n base -c defaults conda --yes
   conda create -n atlas_ce_env python=3.6 --yes
fi

if [[ `which python` != '$HOME/miniconda/bin/python' ]]; then
  # activate the environment
  eval "$(conda shell.bash hook)"
  conda activate atlas_ce_env
fi

echo "using python from `which python`"

if [ ! -f atlas_ce_installer.py ]; then
   wget https://s3.amazonaws.com/foundations-public/atlas_ce_installer.py
fi

MAIN_PATH=`which python | grep -o '^.*atlas_ce_env'`/lib/python3.6/site-packages/atlas-server/

if [ ! -d ${MAIN_PATH} ]; then
   yes | python atlas_ce_installer.py

 # ip fix
 echo -e "import urllib.request\nexternal_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')" > ${MAIN_PATH}/new_main.py
 cat ${MAIN_PATH}/__main__.py >> ${MAIN_PATH}/new_main.py
 sed -i 's/"localhost"/f"\{external_ip\}"/g' ${MAIN_PATH}/new_main.py
 sed -i 's@localhost:@\{external_ip\}:@g' ${MAIN_PATH}/new_main.py
 mv ${MAIN_PATH}/new_main.py ${MAIN_PATH}/__main__.py
fi

if [[ `sudo lsof -i:5555` == '' ]]; then
   atlas-server start > /dev/null 2>&1 &
fi

cd
mkdir atlas-tutorials && cd atlas-tutorials
git clone https://github.com/DeepLearnI/auction-price-regression-tutorial.git

```
2. Next up, running `bash install_atlas.sh` will install Atlas and start it running within Docker
3. Next we'll source the conda environment created by Atlas by running `source ~/.bashrc` and then `conda activate atlas_ce_env`

Now Atlas is running and you'll have access to both the `foundations` and `atlas-server` CLI.

You should now be able to view the Atlas Dashboard by going in your browser to `<external.ip.of.your.instance>:5555`. If you ever need to find the IP of your instance you can find it on your GCP console <a target="_blank" href="https://console.cloud.google.com/compute/instances">instance list</a>).

![SSH into instance](assets/images/gcp-ssh-ip.png)

In the dashboard's project page your should see a project that has been run once. These projects were baked into the script to help get started.

### Run our first Atlas job

If this is your first time using Atlas, you can try run a simple job with the following steps. Or you can just skip ahead to setting up GCP to remotely work with VSCode below.

We can run one of our demo projects to try out how the `foundations` CLI works.

* `cd atlas-tutorials/auction_price_regression_tutorial`
* Run `foundations submit scheduler . driver.py`
* Go back to the Atlas GUI in your browser, and you should see the new job we've just run

For more information on the Foundations CLI read our CLI section, or run `foundations --help`.

We've now successfully setup an Deep Learning VM instance with Atlas! In the next section we'll go over running jobs on GCP with VSCode.

## Running jobs remotely via VSCode

A really easy to develop with Atlas locally in VSCode, while having the power of a cloud GPU, is the setup remote deployment in VSCode. While we also love PyCharm's remote deployment, it's not free, so we'll just use VSCode. This will allow for our code to be synced with our instance, and simply fun `foundations submit ...` commands to run jobs.

Requirements:

* Install <a target="_blank" href="https://code.visualstudio.com/">VSCode</a>

First, open up VSCode, and we'll install the <a target="_blank" href="https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh">Remote - SSH plugin</a> that will allow us to open code from the remote instance in VSCode

![VSCode plugin ](assets/images/vscode-install-plugin.png)
First, open up VSCode, and we'll install the <a target="_blank" href="https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh">Remote - SSH plugin</a> that will allow us to open code from the remote instance in VSCode:

- Open extensions via the left bar menu (or by pressing `shift + cmd + X`)
- Search for `remote-ssh`
- install the plugin

![VSCode plugin ](assets/images/vscode-install-plugin.png)

Before we connect to the host in VSCode, let's open the SSH config file, to add this instance to our SSH Config, to easily allows VSCode to connect to our instance.

* Open `~/.ssh/config` (Create it if it does not exist)

Add the following lines:

```
Host <my.gcp.ip.address>
 IdentityFile ~/.ssh/google_compute_engine
 User <username>
```

Once the plugin is installed and the SSH config is updated, open the Command Palette and select "Remote-SSH: Connect to Host".

* Open command prompt in VSCode: `Cmd + Shift + P` (or click green "Open Remote Window" botton, bottom left of VSCode)
* Search for `remote-ssh`
* Select `Remote-SSH: Connect to Host` from the menu
* Select your instance ip address

It should open a new VSCode window where we'll be able to select "File" > "Open..." and then select a directory from our instance to open. In our case we can select our `atlas_tutorials/auction_price_regression_tutorial` project which will then open up in VSCode in a new window.

At the menu bar at the top of VSCode window we'll select the "Terminal" > "New Terminal". Choose "bash" from the drop down that will give us bash shell access to GCP.

* cd into `atlas-tutorials/auction_price_regression_tutorial`
* Activate the environment with `conda activate atlas_ce_env`
* Let's test that we can run a job with  `foundations submit scheduler . driver.py`
* You should see this job in the Atlas GUI

![vscode shell ](assets/images/gcp-vscode.png)

We're now set! You can now open the files and adjust as you wish, or you can start on your own project. To understand more about the `auction_price_regression` project, you can check out the full tutorial in the **Tutorial** section of the docs.

If you're looking for more detailed docs on setting up VSCode to remotely run code, Microsoft has a good setup <a target="_blank" href="https://code.visualstudio.com/docs/remote/ssh#_remembering-hosts-you-connect-to-frequently">guide</a> with much more detail.

## Tear down GCP instance

It's important to be aware that after the instance has been spun up you will incur costs on your account. There are two options: either stop the instance (which will mean costs are minimal to keep your storage around), or throw away the instance completely.

To stop or terminate the instance:

* Go to your VM instances console
* Find your instance > click either Delete or Stop

![Review ](assets/images/gcp-stop-instance.png)

That's it, we've successfully spun up a GPU instance and run a few jobs remotely from VSCode!

You can now either start your own projects, or look at some of our more advance tutorials to explore more of Atlas.

### Questions

If you have any thoughts or feedback about setting up Atlas on GCP we're always happy to help answer questions on our <a href="https://dessa-community.slack.com/join/shared_invite/enQtNzY5MTA3OTMxNTkwLWUyZDYzM2JmMDk0N2NjNjVhZDU5NTc1ODEzNzJjMzRlMDcyYmY3ODI1ZWMxYTQ3MzdmNjcyOTVhMzg2MjkwYmY" target="_blank">Dessa Community Slack</a>!
