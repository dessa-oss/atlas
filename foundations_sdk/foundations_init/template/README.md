# Foundations project

This project template was generated with `foundations-init`. In this project you'll find the following structure:

### Config

```
/config
	default.config.yaml
```

Configurations define how your job will run. This uses the local deployment type as default.

### Project code

```
/project_code
	driver.py
	model.py
```

The `project_code` directory is where all your model code should go, as well the driver file, which tells Foundations how to structure stages.

The driver should be used to set up the experiment. This is where you'll define stages for your experiments.

The model file is where your stages (python functions) will live.

### Post processing

```
/post_processing
	results.py
```

If you want to read and interact with experiments you've run, you'll interact and analyze experiment results within the `post_processing` directory.

### Data

```
/data
```

This is where you'll put the data to use in your model.

### Additional Resources

Step-by-step guide: [https://github.com/DeepLearnI/foundations/blob/master/documentation/STEPBYSTEPGUIDE.md](https://github.com/DeepLearnI/foundations/blob/master/documentation/STEPBYSTEPGUIDE.md)
API docs: [https://dessa-foundations.readthedocs-hosted.com/en/latest/](https://dessa-foundations.readthedocs-hosted.com/en/latest/)