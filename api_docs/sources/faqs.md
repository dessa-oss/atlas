<h1>Foundations FAQ: Frequently Asked Questions</h1> 

<h2>Foundations Setup</h2>
* [What software dependencies does Foundations require to set up?](../faqs/#what-software-dependencies-does-foundations-require-to-set-up)  
* [What components does Foundations have?](../faqs/#what-components-does-foundations-have)
* [I don’t have access to the source code, how do I install Foundations?](../faqs/#i-dont-have-access-to-the-source-code-how-do-i-install-foundations)
* [Which whl files do I need? What are the differences between them?](../faqs/#which-whl-files-do-i-need-what-are-the-differences-between-them)
* [Do I have to use virtualenv when installing Foundations?](../faqs/#do-i-have-to-use-virtualenv-when-installing-foundations)
* [I installed both the GUI and REDIS locally, but I don’t see any projects when running jobs?](../faqs/#i-installed-both-the-gui-and-redis-locally-but-i-dont-see-any-projects-when-running-jobs)  

<h2>Foundations SDK</h2>
* [Does Foundations support hyperparameter optimizations?](../faqs/#does-foundations-support-hyperparameter-optimizations)
* [Can I use custom libraries mentioned outside my ML project?](../faqs/#can-i-use-custom-libraries-mentioned-outside-my-ml-project)  
* [What is caching in Foundations?](../faqs/#what-is-caching-in-foundations)
* [Is there a default project name when I run a job?](../faqs/#is-there-a-default-project-name-when-i-run-a-job-i-forgot-to-specify-a-project-when-i-deployed-a-job)
* [Can I use stages as part of other objects or data structures and use those as inputs into other stages?](../faqs/#can-i-use-stages-as-part-of-other-objects-or-data-structures-and-use-those-as-inputs-into-other-stages)
* [How can I filter my results returned from get_metrics_for_all_jobs?](../faqs/#how-can-i-filter-my-results-returned-from-get_metrics_for_all_jobs)
* [Is there a way to get a visual representation of the directed acyclic graph (DAG) of the stages I’ve defined in my job?](../faqs/#is-there-a-way-to-get-a-visual-representation-of-the-directed-acyclic-graph-dag-of-the-stages-ive-defined-in-my-job)

<h2>Foundations Job Deployments</h2>
* [What happens in a job deployment? What files and directories are shipped?](../faqs/#what-happens-in-a-job-deployment-what-files-and-directories-are-shipped)  
* [How does Foundations manage packages when deploying jobs?](../faqs/#how-does-foundations-manage-packages-when-deploying-jobs)
* [How do I get the logs for a remote deployed job?](../faqs/#how-do-i-get-the-logs-for-a-remote-deployed-job)
* [How do I track the status of my job?](../faqs/#how-do-i-track-the-status-of-my-job)
* [Does Foundations support GPU deployments?](../faqs/#does-foundations-support-gpu-deployments)
* [What is a global environment configuration vs a project-specific environment configuration?](../faqs/#what-is-a-global-environment-configuration-vs-a-project-specific-environment-configuration)
* [What are the differences between running a job locally versus remotely?](../faqs/#what-are-the-differences-between-running-a-job-locally-versus-remotely)
* [What remote deployments does Foundations support?](../faqs/#what-remote-deployments-does-foundations-support)
* [Can I store my job results or cache in a different remote location than where I run my job?](../faqs/#can-i-store-my-job-results-or-cache-in-a-different-remote-location-than-where-i-run-my-job)
* [Is there a way to run a series of batch jobs whose parameters depend on the results of previous jobs?](../faqs/#is-there-a-way-to-run-a-series-of-batch-jobs-whose-parameters-depend-on-the-results-of-previous-jobs)
* [How do I clear single jobs from the Redis Queue so they don’t show up in the results? How do I clear all jobs?](../faqs/#how-do-i-clear-single-jobs-from-the-redis-queue-so-they-dont-show-up-in-the-results-how-do-i-clear-all-jobs)

<h2>Foundations Security</h2>
* [What kind of security features does Foundations have?](../faqs/#what-kind-of-security-features-does-foundations-have)
* [What open ports does Foundations have?](../faqs/#what-open-ports-does-foundations-have)

---
<h1>Foundations Setup</h1>

####What software dependencies does Foundations require to set up?
| Software        | Package           | License  |
| :------------- |:-------------| :-----|
|Serializing and de-serializing python objects	|Dill ; version 0.2.8.2	|BSD License
|Data storage	|Redis; version 2.10.6|	BSD License
|Data analysis	|Pandas; version 0.23.3	|BSD License
|YAML parser	|Pyyaml; version 3.13	|MIT License
|Python based sftp	|Pysftp; version 0.2.8	|BSD License
|A Python implementation of SSHv2	|Paramiko; version 2.4.1|GNU Lesser General Public License v2.1
|Python based testing	|Mock; version 2.0.0	|BSD License
|Python based testing	|Freezegun; version 0.3.8	|Apache Software License 2.0
|Python based REST API builder	|Flask-restful; version 0.3.6	|BSD License
|Python based Cross Origin Resource Sharing	|Flask-cors; version 3.0.6|	MIT License
|Static site generator	|Mkdocs; version 1.0.4	|BSD License
|Python based promise objects creation|	Promise; version 2.2.1	|MIT License
|Pretty-print tabular data| Tabulate; version 0.8.3 |MIT License
|Python Slack Client| Tabulate; version 0.8.3 |MIT License
|Container based deployment	|Docker ; version 18.09.0|	Apache Software License 2.0
|Scientific computing	|Numpy ; version 1.16.0	|BSD License
|Python based virtual environment creation|	Virtualenv; version 16.0.0	|MIT License

---
####What components does Foundations have?
Foundations contains the following components:  

* GUI - Dockerized web application to view running/completed jobs for various projects  
* SDK - Primary interface to use Foundations with, directly integrates into your model development code and simplifies experiment management  
* Redis - Tracks job metadata and acts as a queue for managing Foundation job deployments  
* Scheduler - For remote deployments, Foundations also includes the scheduler, which is used for job orchestration and management. Setup will vary based on infrastructure and will be handled by the Dessa integrations team.

---

####I don’t have access to the source code, how do I install Foundations?
Foundations can be installed directly with the python wheel files, which are provided by Dessa. To install them, simply run `python -m pip install -U <absolute-path-to-downloaded-whl-file>` for each of the wheel files provided. More information can be found in our [Installation Guide](../start_guide/).

---

####Which whl files do I need? What are the differences between them?
Dessa will help provide the necessary whl files needed to get Foundations up and running on your system depending on your infrastructure. This is because different deployment environments may not require all available whl files, which are essentially plugins for different setups. For example, if you are running experiments through GCP, you will likely not need the AWS plugin.

---

####Do I have to use virtualenv when installing Foundations?
While not mandatory, we highly recommend using a dependency/package manager when installing Foundations. This is because different ML projects will likely need different packages and package versions. Having a package manager to simply switch between different environments makes model development easier to manage. We recommend using virtualenv; however, other package managers such as Anaconda/Conda are also viable options.

---

####I installed both the GUI and REDIS locally, but I don’t see any projects when running jobs?

If you are seeing a 500 error when accessing the GUI, this is most likely due to the GUI server not finding the right REDIS_URL. You can find information on how to setup the REDIS_URL environment variable [here]. However, if you are seeing “No projects available” on the GUI, it’s possible that there are multiple installations of Redis running on the machine (ex: Homebrew). We recommend to stop other instances and use the docker version.

---
<h1>Foundations SDK</h1>

####Does Foundations support hyperparameter optimizations?
Yes! Foundations can perform hyperparameter tuning with the Hyperparameter object and search methods. These allow users to specify values or distributions they would like to hyperparameters to iterate over and Foundations will automatically handle the deployments and management of these jobs with the different combinations to identify the optimal hyperparameter values. Check out the documentation [here](../stage_search/) or our hyperparameter example [here](../hyperparameter_mnist/) for more information.

---

####Can I use custom libraries mentioned outside my ML project?
The use of custom libraries is supported. To use custom libraries, they will need to be added to the Foundations project directory and referenced accordingly in the model or driver files. This is because when the job is deployed, Foundations will bundle the entire project directory (including the custom libraries) and send them to the specified machine. By placing the custom libraries in the project directory, this ensures that the files are available when the code is run.

---
####What is caching in Foundations? 
Caching is a feature of Foundations where stage results are kept in a cache so they can be re-used without having to run those stages again. The path of this storage location can be configured on the deployment environment [configuration file](../configs/#cache-configurations). When running the Foundations pipeline, this can be enabled on stages with [enable_caching](../running_stages/#enable_caching)

---
####Is there a default project name when I run a job?
Foundations deploys jobs under the “default” project if no project name is specified

---

####Can I use stages as part of other objects or data structures and use those as inputs into other stages?
Unfortunately this use case is likely to fail. A stage does not act like the object that it's proxying and by treating it as an attribute will result in other stages not properly handling it.

---

####How can I filter my results returned from get_metrics_for_all_jobs?
The function get_metrics_for_all_jobs returns a pandas dataframe of all jobs and metrics for a given project, which supports manipulation and filtering. Additional information on dataframes can be found [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)

---
####Is there a way to get a visual representation of the directed acyclic graph (DAG) of the stages I’ve defined in my job? 
Unfortunately this is not supported at the moment; however, this is on our radar and is something you can expect in the near future!

---

<h1>Foundations Job Deployments</h1>

####What happens in a job deployment? What files and directories are shipped?
When a job is deployed with Foundations, the entire project directory, including any additional libraries or data objects, gets bundled together into a tarball and transferred to the specified environment via SSH. The job is then unpacked and additional packages from the requirements.txt file are installed. The driver code is then executed and the Foundations pipeline is run. 

---

####How does Foundations manage packages when deploying jobs?
For deployments, additional packages or custom libraries need to be specified using a requirements.txt file in the project directory. This indicates to the deployment machine server to download those additional dependencies before running the job. Check out our example [here](../remote_deployment_example/#2-specify-additional-remote-dependencies) on how to setup the requirements.txt file. 

---

####How do I get the logs for a remote deployed job?
Job logs can be retrieved through the deployment object with [get_job_logs](../job_logs/) 

---
####How do I track the status of my job?
Once a job is deployed either remotely or locally, the status can be retrieved through the deployment object with `get_job_status()`. More information on tracking deployments can be found [here](../tracking_deployment/)

---
####Does Foundations support GPU deployments?
Yes, if the infrastructure has GPUs enabled and the correct libraries are used (ie: tensorflow-gpu)

---
####What is a global environment configuration vs a project-specific environment configuration?
Global configurations are a way to simplify storing common environment configurations that may span multiple projects. For example, if multiple projects are all going to be deployed to the same GCP environment, only one configuration file is needed and can be accessed by any project directory on the machine. This way, multiple projects can use the same deployment environment without needing to manage individual configurations per project. Global configurations can be setup by placing configurations in the `~/.foundations/config` directory. Project-specific environments are used when specific deployment environments are used for testing (ex: testing a model on the local machine first) rather than shared across multiple projects.

---
####What are the differences between running a job locally versus remotely?
Running a job locally uses the resources on the local machine to execute the code, typically in the same directory as the Foundations project as well. Remote jobs bundle your code and transfer it to another environment to be unpacked and run on the remote machine’s resources. For remote deployments, Foundations leverages the scheduler, which orchestrates job execution and storage.

---
####What remote deployments does Foundations support?
Foundations supports deployments to AWS, GCP, or other remote machines via SSH access. These are configurable by setting up environment configuration files and selecting the appropriate one when deploying. More information on remote deployments can be found [here](../configs/).

---
####Can I store my job results or cache in a different remote location than where I run my job?
As long as the necessary credentials are setup across different environments, Foundations can support storage of job results and cache to different remote locations. This can be setup in the deployment configuration file by specifying the path with the full URI schema needed to access that remote machine. For example, if you deploy the job locally and want to store the results in GCP, you can specify the path as `gcp://<bucket>/path/to/archive` and Foundations will automatically push results to that specified path. More information on remote deployment paths can be found [here](../configs/#configuration-options)

---
####Is there a way to run a series of batch jobs whose parameters depend on the results of previous jobs?
By using Hyperparameters, parameters can dynamically be generated during runtime between jobs. This means that by properly tracking metrics, hyperparameters and modifying the results dataframe, you could potentially pass the results from one job to the next, assuming the model and stages are the same.

---

####How do I clear single jobs from the Redis Queue so they don’t show up in the results? How do I clear all jobs?
Completed jobs can be archived using the `archive_jobs` function. This removes them from any project results on both the GUI or SDK. In addition, Foundations does not permanently  delete the jobs, but only hides them from appearing again. More information can be found [here](../manage_jobs/#archive_jobs)

---

<h1>Foundations Security</h1>

###What kind of security features does Foundations have?
* NGINX & SSL protected GUI server
* Spiped encryption
* Password protection on GUI and Redis
* [OWASP Top 10](https://www.owasp.org/index.php/OWASP_Top_Ten_Cheat_Sheet) Compliance
* Port Vulnerability Compliance
* [CIS-CAT](https://www.cisecurity.org/cybersecurity-tools/cis-cat-pro/) security benchmarking on client machines
* [Obfuscation](http://pyarmor.dashingsoft.com/) of Foundations Code (SDK)
---
###What open ports does Foundations have?
Across the different Foundations components, there are only three open ports (by default: 22, 6379, 6443). These ports are encrypted and comply with various industry-standard port vulnerability tests. 
