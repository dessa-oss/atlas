# Atlas Multinode & Multiuser AWS Setup Instructions

The following document outlines how to setup and deploy a multi-node compute system that runs Atlas including the Keycloak authentication system to AWS.

This setup is ideal for teams of Machine Learning Engineers who want to run Deep Learning jobs on an AWS compute cluster. 

If you are looking to setup _only for yourself_ without an authentication system follow the steps [here](aws-installation.md).

## Prerequisite
* AWS account for admin

## Setup master node

Atlas will need a master node instance, worker instance node(s), as well as an EFS filesystem.

### Creating master instance on AWS

In order to setup Atlas, we'll first create the master instance that will be in charge of storing and managing the job queue.

### Choose an Amazon Machine Image (AMI)

* Search for the "DeepLearning AMI" that uses Ubuntu 16.04

### Configure an Instance Type

For this page we'll select a *t2 medium* instance type.

Make sure to click **"Next: Configure Instance Details"** to continue provisioning the instance.

### Configure Instance Details

* If your instance does require additional configuration adjust as needed
* Otherwise there are no changes needed here, just click **"Next: Add Storage"**

### Add Storage

We recommend increasing the size of your storage to at least 250GB. Adjust as needed for your expected data.

![Add storage](../assets/images/aws-add-storage.png)

### Add Tags

* No changes, just click **Next: Configure Security Group**

### Configure Security Group

Next, we'll create a new security group to allow for Atlas to securely use a few different ports on our instance. Specifically to allow the Atlas Dashboard UI, REST API, and archive server.

To allow for this add the following 4 new rules:

* Type: `NFS`, port: `2049`, source: `<Name of security group>`
* Type: `Custom TCP`, port: `5555`, source: `My IP` 
* Type: `Custom TCP`, port: `5558`, source: `My IP`
* Type: `Custom TCP`, port: `8443`, source: `My IP`

![Add storage](../assets/images/atlas-team-security-group.png)

Now, click **Review and Launch** to go review our instance before launching. 

### Review Instance Launch

Our instance setup should now look similar to the below.

<!-- ![Review](../assets/images/aws-review-instance-launch.png) -->


* Click "Launch" which should then ask you to create a new key pair
* Select "Create a new key pair" and give it the name "atlas-team" (note: if you've already used this key name before you can either re-use of, or create another unique key name)
* Download the key pair
* Click "Launch Instances"
* It should then redirect you to the Launch Status page
* Beside "The following instance launches have been initiated" you should see your new instance ID. Click the ID to go to the **Instances** page
* You can find the public IPv4 address of the instance in the lower **Description** panel.

![aws now launching](../assets/images/aws-now-launching.png)

You should then be able to use your downloaded `.pem` key to then SSH into the instance to check that everything is setup.

Run `chmod 400 <key_name>.pem` on your key before SSH'ing to give it the proper permissions. We also recommend that you move the key to your `~/.ssh/` directory.


## Create an EFS filesystem

We'll also need to setup an EFS filesystem that we can use as a central storage location.

* When configuring the EFS filesystem for each availability zone add it to the security group that was  previously created and added to the master instance.

![efs creation](../assets/images/atlas-team-efs.png)


* After creation click on **On-premise mount instructions**, and it will provide a few commands that will mount the filesystem. You'll need the `sudo mount -t nfs4...` command in a few steps, so either copy it or keep this tab open for easy access.

![mount efs](../assets/images/mount-instructions.png)

## Installing and setting up Atlas

The following outlines how to setup Atlas on the master node:

* SSH into the master instance `ssh -i /path/to/key/<key_name>.pem  ubuntu@ipv4.of.ec2.instance`

* Download the installer onto the instance (both the atlas_installer.py and atlas_team.tgz). These two files are provided by Dessa.

* Create a conda environment: `conda create -y -n atlas-team python=3.6.8`

* Run `echo ". /home/ubuntu/anaconda3/etc/profile.d/conda.sh" >> ~/.bashrc` and then `source ~/.bashrc` to make sure conda can be used in your shell

* Activate the conda environment `conda activate atlas-team`

* Run the installer: `python atlas_installer.py -dl`

* Backup `~/.foundations` directory: `cp -r ~/.foundations ~/.BACK_foundations`

* Mount the EFS system to `~/.foundations`. Do this by using the mount command that was provided after creating the EFS filesytem: `sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-b563e834.efs.us-east-1.amazonaws.com:/ ~/.foundations`

* Copy the content of the backed-up directory back: `cp -r ~/.BACK_foundations/* ~/.foundations`

* Create a directory as follows: `mkdir ~/f9s_work_dir`

### Updating master node configurations

**~/.foundations/config/local_docker_scheduler/database.config.yaml**

* Update to use the Master nodes Private IP in all 4 `host` fields and `5556` in all `port` fields

**~/.foundations/config/local_docker_scheduler/tracker_client_plugins.yaml**

* Update to use the Master nodes Private IP in the `host` field and `5556` in the `port` field

**~/.foundations/config/local_docker_scheduler/worker_config/execution/default.config.yaml**

* Replace `atlas-ce-tracker` with the Master nodes Private IP and `6379` with `5556`

**~/.foundations/config/local_docker_scheduler/worker_config/submission/scheduler.config.yaml**

* Replace `atlas-ce-local-scheduler` with the Master nodes Private IP and the value for `working_dir_root` to be `/home/ubuntu/f9s_work_dir`

**~/.foundations/config/submission/scheduler.config.yaml**

* Change `working_dir_root` to be `job_store_dir_root`

* Add a field `working_dir_root: /home/ubuntu/f9s_work_dir` at the bottom

### Starting Atlas Server

Set environment variables

* `export HOST_ADDRESS=http://<MASTER-NODE-PRIVATE-IP>:5000/`

* `export REDIS_ADDRESS=<MASTER-NODE-PRIVATE-IP>`

* `export NUM_WORKERS=0`, which will mean this master node will not be used for computing jobs. Default is 1 if not provided

* Run `atlas-server start` to start the Atlas server

### Log into Atlas' authentication system

Atlas runs a Keycloak authentication server for managing users and login.

* Login to Keycloak via the admin console: `https://<master_node_external_ip>:8443`. When first spun up the username and password will both `admin`

* We recommend changing the admin password upon first login

* You can also create a user at this point. To do so, in the admin console go to Users > Add User

### Add new users

After logging into the authentication system, the admin user can create new Atlas users:

* In the sidebar, go to `Users` > `Add user`

* Enter information for the new user and save

* Go to `Credentials` tab to configure a password for the new user


## Setup worker node

For our multi-node system, we can spin up as many worker instances as needed. Below we'll walk through setting up on one instance. Repeat as needed.

1. Create a Worker EC2 instance using the Ubuntu 16.04 Deeplearning AMI (p2.xlarge recommended). You can follow the previous steps above with respect to adding to the same Inbound Rules and Security group during instance configuration.

![Instance type](../assets/images/aws-instance-type.png)

2. SSH into the worker instance `ssh -i /path/to/key/<key_name>.pem ubuntu@ipv4.of.ec2.instance`

3. Download the installer onto the instance (both atlas_installer.py and atlas_team.tgz). These two files are provided by Dessa.

4. Create a conda environment: `conda create -y -n atlas-team python=3.6.8`

5. Activate the conda environment: `conda activate atlas-team`

6. Run the installer: `python atlas_installer.py -dl`. Using `-dl` tells the Atlas installer: 

    `-d`: no download

    `-l`: use latest

7. Mount the EFS system to `~/.foundations`. Do this by using the mount command that was provided after creating the EFS filesytem: `sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-b563e834.efs.us-east-1.amazonaws.com:/ ~/.foundations`

8. Set environment variables
    * `export HOST_ADDRESS=http://<NODES-IP>:5000/`
    * `export REDIS_ADDRESS=<MASTER-NODE-PRIVATE-IP>`
    * `export NUM_WORKERS=1`

9. Run `atlas-server start` to start the Atlas server


## Getting users set up

Once both the master and worker(s) instances are setup to handle job submission, we can now get users submitting jobs. The user will need to 1) install Atlas, and 2) have proper submission configuration file.

The Atlas dashboard can be accessed via: `<master_external_ip>:5555`.

The following steps outline the configurations for a user to have on their client machine in order to submit jobs:

* The admin will need to create an account for any new user. This can be done at the Keycloak GUI at `https://<master_node_external_ip>:8443/auth/`. To do so, in the admin console go to Users > Add User

!!! note
    A user login session is set to 5 minutes by default, meaning the token will expire and user will be logged out. To change this go to the Keycloak Admin dashboard at `https://<master_node_external_ip>:8443` > Administration Console.
    
    Once logged in Realm Settings > Tokens > Access Token Lifespan to adjust the expiration.

* Install Atlas SDK into a new conda environment on the user's machine. This should allow the user to have access to the `foundations` CLI

* The user will need to add a new configuration file that will be need to be provided by the integrations person. This file is generated on the master node in `~/.foundations/config/local_docker_scheduler/worker_config/submission/scheduler.config.yaml`

* Update the `scheduler_url` value with the master node's external IP, and the port should `5558` 


Example of `team.config.yaml`:

    cache_config:
        end_point: /cache_end_point
    container_config_root: /home/ubuntu/.foundations/config/local_docker_scheduler/worker_config
    job_deployment_env: local_docker_scheduler_plugin
    job_results_root: /home/ubuntu/.foundations/job_data
    scheduler_url: http://<master_node_external_ip>:5558
    working_dir_root: /home/ubuntu/f9s_work_dir

The `team.config.yaml` file should be put on the user's machine at `~/.foundations/config/submissions/`.

To test that job submission is working, the user can submit a job with the following steps:

* On the user's machine, make sure the conda environment is enabled with Atlas installed, then run `foundations init <project_name>` to create a simple project with Foundations' scaffolding

* `cd` into the project directory, and run `foundations submit team . main.py`, where `team` is the first part of the name of the config file we just added

* This should submit a job to our master node, which should then schedule that to the worker.

* The user can now load the Atlas Dashboard, and should be able to see the job

![first job](../assets/images/first_atlas_project.png)

You should be all setup with Atlas Team now. To conclude, here's what we've done:

* A master machine for orchestrating job execution
* A worker node for executing jobs
* An EFS filesystem as a central storage
* Setup a user to submit jobs

## Cleanup and removing nodes

To remove a specific worker node, just terminate the specific worker instance from the AWS console.

To shut down Atlas Team from AWS. Make sure to shut down all instances and related infrastructure when wanting to stop incurring all AWS costs. Make sure to remove all of the following:

- Master node
- Worker node(s)
- EFS filesystem
- Security group