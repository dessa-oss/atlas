from foundations_rest_api.global_state import app_manager
from foundations.global_state import deployment_manager

for thing in deployment_manager.scheduler().get_job_information():
    print(thing)

app = app_manager.app()
app.run(port=37722)

