# Instructions for deploying the Foundations UI

1. Run ```./start_foundations_ui.sh``` in terminal from the ```foundations/foundations_ui``` folder. 

    - This script will start up the foundations REST API server on [http://localhost:37722](http://localhost:37722) and the foundations ui webapp on [http://localhost:3000](http://localhost:3000).  
    - The webapp should automatically open in your default browser. If it doesn't, navigate to http://localhost:3000 in your browser.   
    - Press Ctrl-C to stop the foundations REST API server and the foundations ui webapp.   

2. Remote Deployment

    - To run jobs on a remote execution environment, you'll need to make a `ui.config.yaml` file that duplicates the `config.yaml` settings of the job you are running. This will tell Foundations where to send your job.

    - *Example*: if you're running the logistic_regression (or any other) example locally, copy the `foundations/examples/local_deploy_default.config.yaml` file and paste it into the `foundations/foundations_ui` folder.