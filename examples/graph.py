import foundations

# foundations.config_manager["error_verbosity"] = "VERBOSE"
# foundations.config_manager["log_level"] = "INFO"

def bad():
    return 1 / 0

bad = foundations.create_stage(bad)
result = bad()

result.run_same_process()