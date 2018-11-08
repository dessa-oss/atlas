# Windows Instructions

**Read [the start guide](STARTGUIDE.md) first if you haven't already**

## Setting up local configuration

In order to get Foundations working correctly on Windows, you'll have to ensure that you environment is set up correctly. When installing software dependencies (such as Anaconda or Git), the default installation settings should be sufficient to get things working.

### Deploying jobs
As per [the start guide](STARTGUIDE.md#environment-and-dependencies) you should able to use an example configuration to start deploying jobs using Foundations. 

The most important change in any configuration is the `shell_command` key. Setting this value allows Foundations to be able to understand how to execute the shell scripts that are required for running jobs. The recommended value for this is `C:\\Program Files\\Git\\bin\\bash.exe` which is in the default install location for git for Windows. If you changed this path during installation, you will have to change this value respectively.

### Local deployment

An [example configuration](../examples/example_configs/local_windows.config.yaml) has been provided as a starting point for running jobs locally on Windows. Please take note that when running jobs locally on Windows, all paths must be prefixed by the Windows partition (ie `C:\\`) that they are located on. 

### Deploying remote jobs from Windows
It is also important to understand that if you are deploying from Windows to the Foundations scheduler that the paths defined in you configuration must retain their Linux form. For example, we would use `/path/to/remote/jobs` instead of `C:\path\to\remote\jobs`