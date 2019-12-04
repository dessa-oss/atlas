import foundations

print("I should not print out because the worker image is invalid")
foundations.log_metric("Worker", "invalid image")
