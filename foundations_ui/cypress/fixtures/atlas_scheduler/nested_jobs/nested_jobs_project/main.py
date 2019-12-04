import foundations

foundations.log_metric('name', 'job1')

deployment = foundations.submit(command=["job2.py"])
deployment.wait_for_deployment_to_complete(wait_seconds=10)
