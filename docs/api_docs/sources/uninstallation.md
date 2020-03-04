# Uninstallation

We are sad to see you go, but hope you enjoyed your time using Atlas. 

Hopefully you could send us feedback as to why you are no longer using Atlas: {==[foundations@dessa.com](mailto:foundations@dessa.com)==}

### Docker image removal

 1. Run `docker images | grep atlas` and make sure that you are not going to delete any non-Atlas Docker images
 2. Run `docker images | grep atlas | awk '{print $3}' | xargs docker rmi -f`
 
### Python package removal

 1. Run `pip list | grep foundations` and make sure that you are not going to delete any non-Atlas Python packages
 2. Run `pip list | grep foundations | awk '{print $1}' | xargs pip uninstall -y`
 
### Foundations home directory removal

!!! danger "Data removal"
    Any jobs that you have run are archived within `~/.foundations/job_data/archive`. If you have code or data that you wish to keep around, you should copy them to a safe location.
    
    Additionaly, any metadata is stored in a Redis backup file in `~/.foundations/database/dump.rdb`. You may want to back this up if there is important information from jobs that have run.

 1. Run `rm -rf ~/.foundations`