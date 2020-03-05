# Atlas on AWS

Being able to run Atlas on AWS means access to GPUs and faster results. In this tutorial we'll walk through setting up and running jobs on AWS with Atlas.

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
  <iframe src="https://www.youtube.com/embed/fs4ivj5lp64?start=9" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

Requirements

* An AWS account


## Create instance

First, let's go to the AWS developer console. Sign in, and then we'll create a new instance: <a target="_blank" href="https://aws.amazon.com/console/">AWS console</a>

Go to Services > EC2, then click the **"Launch Instance"** button to start setup.

!!! note
    The custom AMI we'll be using for this tutorial is only available in us-east (Ohio), Canada (Central), and EU (Ireland), so you'll need to switch to one of those regions before creating an instance.

### Step 1: Choose an Amazon Machine Image (AMI)

Let's use the custom Atlas AMI, to do this:

* Select "Community AMIs" on the left sidebar
* Search for "Atlas"
* Select the AMI that says "Atlas Community Edition on Deep Learning AMI for Ubuntu
"

Our custom AMI is just AWS's Deep Learning AMI (Deep Learning AMI (Ubuntu 16.04) Version 24.2) with Atlas added on top of it.

!!! note
    Once the instance has been finalized and spun up, costs will be incurred. Please follow the tear down steps at the bottom of this guide to minimize this.

### Step 2: Configure an Instance Type

For this page we'll select a *p2.xlarge* instance type, as we want some a GPU to train with. We recommend a P2 instance as it a good balance between performance and cost, but if you are looking for more power you can select a P3 instance.

![Instance type](assets/images/aws-instance-type.png)

Make sure to click **"Next: Configure Instance Details"** to continue provisioning the instance.

### Step 3: Configure Instance Details

* If your instance does require additional configuration adjust as needed
* Otherwise there are no changes needed here, just click **"Next: Add Storage"**

### Step 4: Add Storage

We recommend increasing the size of your storage to at least 250GB, as the base AMI image is already ~80GB. Adjust as needed for your expected data.

![Add storage](assets/images/aws-add-storage.png)

### Step 5: Add Tags

* No changes, just click **Next: Configure Security Group**

### Step 6: Configure Security Group

Next, we'll create a new security group to allow for Atlas to securely use a few different ports on our instance. Specifically to allow the GUI, REST API, and archive server.

To allow for this:

* Add 3 new rules, with ports for 5555, 5557, and 5959
* Adjust the "Source" to **My IP** for each rule

![Add storage](assets/images/aws-security-group.png)

Now, click **Review and Launch** to go review our instance before launching. 

### Review Instance Launch

Our instance setup should now look similar to the below.

![Review ](assets/images/aws-review-instance-launch.png)


* Click "Launch" which should then ask you to create a new key pair
* Select "Create a new key pair" and give it the name "atlas" (note: if you've already used this key name before you can either re-use of, or create another unique key name)
* Download the key pair
* Click "Launch Instances"
* It should then redirect you to the Launch Status page
* Beside "The following instance launches have been initiated" you should see your new instance ID. Click the ID to go to the **Instances** page
* You can find the IPv4 address of the instance in the lower **Description** panel.

![aws now launching](assets/images/aws-now-launching.png)

You should then be able to use your downloaded `.pem` key to then SSH into the instance to check that everything is setup.

Be sure to run `chmod 400 <key_name>.pem` on your key before SSH'ing to give it the proper permissions. We also recommend that you move the key to your `~/.ssh/` directory.
 
`ssh -i /path/to/key/<key_name>.pem  ubuntu@ipv4.of.ec2.instance`

**You should expect to wait ~30 seconds when you first SSH in.**

The instance will run a few commands which includes activating a conda environment that contains `atlas-server` and `foundations`. It also runs `atlas-server` so all the services for Atlas are running.

When you SSH into the instance, `atlas-server` will start, but you can put it into a background process with `ctrl + c`, to then be able to run other commands.

You should also now be able to see the GUI. In your browser go `<ipv4.of.ec2.instance>:5555` and you should see the Atlas project page with two projects that have each been run once. These projects were baked into the AMI to help get started.

### Run our first Atlas job

If this is your first time using Atlas, you can try run a simple job with the following steps. Or you can just skip ahead to setting up AWS to remotely work with VSCode below.

We can run one of our demo projects to try out how the `foundations` CLI works.

* `cd atlas_tutorials/auction_price_regression_tutorial`
* Run `foundations submit scheduler . driver.py`
* Go back to the Atlas GUI in your browser, and you should see the new job we've just run

For more information on the Foundations CLI read our CLI section, or run `foundations --help`.

We've now successfully setup a P2 instance with Atlas! In the next section we'll go over running jobs on AWS with VSCode.

## Running jobs remotely via VSCode

A really easy to develop with Atlas locally in VSCode, while having the power of a cloud GPU, is the setup remote deployment in VSCode. While we also love PyCharm's remote deployment, it's not free, so we'll just use VSCode. This will allow for our code to be synced with our instance, and simply fun `foundations submit ...` commands to run jobs.

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

It should open a new VSCode window where we'll be able to select "File" > "Open..." and then select a directory from our instance to open. In our case we can select our `atlas_tutorials/auction_price_regression_tutorial` project which will then open up in VSCode in a new window.

At the bottom the VSCode window we'll select the "Terminal" tab, and click the "+" symbol to open a new shell tab. Choose "bash" from the drop down that will give us bash shell access to AWS.

* cd into `atlas_tutorials/auction_price_regression_tutorial`
* Let's test that we can run a job with  `foundations submit scheduler . driver.py`
* You should see this job in the Atlas GUI

![vscode shell ](assets/images/vscode-bash-submit.png)

We're now set! You can now open the files and adjust as you wish, or you can start on your own project. To understand more about the `auction_price_regression` project, you can check out the full tutorial in the **Tutorial** section of the docs.

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
