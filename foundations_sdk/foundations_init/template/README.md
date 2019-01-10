# Foundations project

This project template was generated with `foundations-init`. In
this project you'll find the following structure:

### Config

/config
	default.config.yaml

Configurations define how your job will run. This uses the local deployment type as default. Find more information about configs and other deployment types on our docs page.

### Project code

/project_code
	driver.py
	README.md

The project code directory is where all your model code should go, as well the driver application which tells Foundations how to structure stages.

### Post Processing

/post_processing
	results.py

If you want to read and interact with results you've run, you'll add the code to the post processing directory.

### Data

/data

Where data sits.

## Requirements

- redis running