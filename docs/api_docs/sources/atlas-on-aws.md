# Atlas on AWS

The beauty of the cloud is that everyone can have easy access to really powerful machines.

Being able to run Atlas on AWS means access to GPUs and faster results. 

In this tutorial we will cover the following: 

1. Setting up an AWS instance for DeepLearning 
2. Setting up Atlas 
3. Configuring VSCode to be able to run remote jobs 
4. Running our first job remotely!

### Requirements

* An AWS account

## Create instance

First, let's go to the AWS developer console. Sign in, and then we'll create a new instance: <a target="_blank" href="https://aws.amazon.com/console/">AWS console</a>

Go to Services > EC2, then click the **"Launch Instance"** button to start setup.

### Step 1: Choose an Amazon Machine Image (AMI)

!!! note
    We will be using AWS's DeepLearning AMI for this tutorial. We recommend using this to begin with unless you have heavy custom requirements. AWS's DeepLearning AMI already includes Python setup using anaconda and comes pre-built with maority of the DeepLearning libraries like Tensorflow. 

    You are welcome to use your own custom instances, just make sure to install Anaconda [here is a great tutorial.](https://www.youtube.com/watch?v=HJ_ayBsZytg). 

Let's use the AWS Deep Learning AMI, to do this:

* Select "AWS Marketplace" from the sidebar
* Search for "AWS Deep Learning AMI"
* Select the AWS AMI with the latest version of Ubuntu.
    * In our case we have selected `AWS Deep Learning AMI (Ubuntu 18.04)`

### Step 2: Configure an Instance Type

For this page we'll select a *p2.xlarge* instance type, as we want some a GPU to train with. We recommend a P2 instance as it a good balance between performance and cost, but if you are looking for more power you can select a P3 instance.

![Instance type](assets/images/aws-instance-type.png)

Make sure to click **"Next: Configure Instance Details"** to continue provisioning the instance.

### Step 3: Configure Instance Details

* If your instance does require additional configuration adjust as needed
* Otherwise there are no changes needed here, just click **"Next: Add Storage"**

### Step 4: Add Storage

We recommend increasing the size of your storage to at least 250GB, as the base AMI image is already quite big. Adjust as needed for your expected data.

![Add storage](assets/images/aws-add-storage.png)

### Step 5: Add Tags

* No changes, just click **Next: Configure Security Group**

### Step 6: Configure Security Group

Next, we'll create a new security group to allow for Atlas to securely use a few different ports on our instance. Specifically to allow the GUI, REST API, and archive server.

To allow for this:

* Add 3 new rules, with ports for 5555, 5557, and 5959
* Adjust the "Source" to **My IP** for all the rules including the SSH rule

!!! note 
    Changing the source to "My IP" means that the field will automatically be populated with the public IPv4 address of your local computer. This acts as a firewall for the instance, ensuring that the only inbound traffic comes from your personal computer. Learn more from the official [AWS guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html).

![Add storage](assets/images/aws-security-group.png)

Now, click **Review and Launch** to go review our instance before launching. 

### Step 7: Review Instance Launch

Our instance setup should now look similar to the below.

![Review](assets/images/aws-review-page.png)

### Step 8: Launch
* Click "Launch" which should then ask you to create a new key pair
* Select "Create a new key pair" and give it the name "atlas" (note: if you've already used this key name before you can either re-use of, or create another unique key name)
* Download the key pair to a folder
* Click "Launch Instances"
* It should then redirect you to the Launch Status page
* Beside "The following instance launches have been initiated" you should see your new instance ID. Click the ID to go to the **Instances** page
* You can find the IPv4 address of the instance in the lower **Description** panel.

![aws now launching](assets/images/aws-now-launching.png)

!!! danger
    💰 Once the instance has been finalized and spun up, costs will be incurred. Please follow the tear down steps at the bottom of this guide to minimize this.

### Step 9: SSH
Make sure you have the `.pem` key from Step 7. 

We should now be able to use your downloaded `.pem` key to then SSH into the instance to check that everything is setup.

* Run `chmod 400 <key_name>.pem` on your key before SSH'ing to give it the proper permissions. 
* [Optional] We also recommend that you move the key to your `~/.ssh/` directory.
* Run `ssh -i <path_to_your_key>.pem  ubuntu@<instance_ipv4>` replacing "<>" with your key file and IPv4 in your terminal. This will connect you to the remote instance.

!!! note
    You should expect to wait ~30 seconds when you first SSH in.

### Installing Atlas 
* You should now be within your AWS instance.
* Create a new directory for Atlas: `mkdir atlas`
* Find a version of Atlas from https://github.com/dessa-oss/atlas/releases that you want to install and run `wget <link_to_installer_file>` to download the installer file to this instance.
*  Create and activate a Python >=3.6 virtual environment using Conda or venv to minimize dependency issues.
    * `conda create --name=atlas python=3.7`
* Ensure you are in the right conda environment, then run the install script `python atlas_installer.py` and follow the instructions.

!!! tip 
    Running `python atlas_installer.py --help` will give you troubleshooting advice if the script isn't working as expected.

!!! tip
    The longest part of the script is pulling the Atlas docker images, if the script fails at this point, 
    you can re-run it using `python atlas_installer.py -dp` to skip over the download and unpacking and go directly to the image pull.

### Run our first Atlas job

* Validate that you are in the same Python environment that was used to run the installation script.
* Run `atlas-server start`

!!! note
    If your instance comes with a GPU, you can ensure Atlas runs with GPU enabled by running `atlas-server start -g`

You should now be able to see the GUI. In your browser go `<ipv4.of.ec2.instance>:5555` and you should see the Atlas project page with two projects that have each been run once. These projects were baked into the AMI to help get started.

If this is your first time using Atlas, you can try to run a simple job with the following steps or you can just skip ahead to setting up AWS to remotely work with VSCode below.

 1. Navigate to where you'd like to create your Atlas project directory.
 2. Run `foundations init hello-atlas` to create an example project.
 3. Navigate into the newly created `hello-atlas` directory.
 4. Run the sample code provided by running `python main.py`.
 5. Head to the GUI to see your experiment!

For more information on the Foundations CLI read our CLI section, or run `foundations --help`.

We've now successfully setup a P2 instance with Atlas! In the next section we'll go over running jobs on AWS with VSCode.

## Running jobs remotely via VSCode

Configuring VSCode to work with a remote instance allows us to code on our own machines, while having the power of a cloud GPU. While we also love PyCharm's remote deployment, it's not free, so we'll just use VSCode. This will allow for our code to be synced with our instance, and simply run `foundations submit ...` commands to run jobs.

Requirements:

* Install <a target="_blank" href="https://code.visualstudio.com/">VSCode</a>

First, open up VSCode, and we'll install the <a target="_blank" href="https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh">Remote - SSH plugin</a> that will allow us to open code from the remote instance in VSCode:

- Open extensions via the left bar menu (or by pressing `shift + cmd + X`)
- Search for `remote-ssh`
- install the plugin

![VSCode plugin ](assets/images/vscode-install-plugin.png)

Before we connect to the host in VSCode, let's open the SSH config file, to add this instance to our SSH Config, to easily allows VSCode to connect to our instance.

* Open `~/.ssh/config` (Create it if it does not exist)

Add the following lines:

```
Host <my.aws.ip.address>
 IdentityFile ~/.ssh/<key_name>.pem
 User ubuntu
```

Let's also give the right permission to our `pem` file using the following command:

```
chmod 400 ~/.ssh/<key_name>.pem
```

Once the plugin is installed and the SSH config is updated, open the Command Palette and select "Remote-SSH: Connect to Host".

* Open command prompt in VSCode: `Cmd + Shift + P` (or click green "Open Remote Window" botton, bottom left of VSCode)
* Search for `remote-ssh`
* Select `Remote-SSH: Connect to Host` from the menu
* Select your instance ip address

It should open a new VSCode window where we'll be able to select "File" > "Open..." and then select a directory from our instance to open. In our case it will be the sample project we made in the "Running your jobs on Atlas" section above.

At the bottom the VSCode window we'll select the "Terminal" tab, and click the "+" symbol to open a new shell tab. Choose "bash" from the drop down that will give us bash shell access to AWS.

* `cd` into your code's repository
* Let's test that we can run a job with  `foundations submit scheduler . driver.py`
* You should see this job in the Atlas GUI

![vscode shell ](assets/images/vscode-bash-submit.png)

We're now set! You can now open the files and adjust as you wish, or you can start on your own project. 

Check out some of the step by step Atlas tutorials to get started on a project:
1. [Auction Price Regression Tutorial](tutorials/auction_price_regression_tutorial.md)
2. [CIFAR Tutorial](tutorials/cifar_tutorial.md)
3. [Image Segmentation](tutorials/image_segmentation_tutorial.md)

If you're looking for more detailed docs on setting up VSCode with AWS, Microsoft has a good setup <a target="_blank" href="https://code.visualstudio.com/docs/remote/ssh#_remembering-hosts-you-connect-to-frequently">guide</a> with much more detail.

## Tear down AWS instance

It's important to be aware that after the instance has been spun up, you will incur costs on your account. There are two options: either stop the instance (which will mean costs are minimal to keep your storage around), or throw away the instance completely.

To stop or terminate the instance:

* Go to your AWS console
* Right click on our P2 instance > "Instance State" > either Terminate or Stop

![Review ](assets/images/aws-stop-instance.png)

That's it! We've successfully spun up a GPU instance, and run jobs remotely, from VSCode.

You can now either start your own projects, or look at some of our more advanced tutorials to explore more of Atlas.

### Questions

If you have any thoughts or feedback about setting up Atlas on AWS, we're always happy to help answer questions on our <a href="https://dessa-community.slack.com/join/shared_invite/enQtNzY5MTA3OTMxNTkwLWUyZDYzM2JmMDk0N2NjNjVhZDU5NTc1ODEzNzJjMzRlMDcyYmY3ODI1ZWMxYTQ3MzdmNjcyOTVhMzg2MjkwYmY" target="_blank">Dessa's Community Slack</a>!
