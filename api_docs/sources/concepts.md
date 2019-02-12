<h1>Foundations concepts</h1>

To understand Foundations you have to understand these basic concepts

### Stage

A stage is a step in the Machine Learning process. It is a functional piece of software that does a specialized task. A stage could be dedicated to loading data, preprocessing, training a model, and so on. Each stage has different input parameters that can be passed from previous stages, return values that can be passed to subsequent stages, and output metrics that can be returned to the user to provide feedback about the stage behavior. In Foundations, stages are created by passing a Python function that does a specialized task to `create_stage()`. See an [example](../stage_creation/#create_stage_example).

### Hyperparameter

A hyperparameter is a configuration value that is external to the model and cannot be estimated from data. It is always set before the learning/training process begins. Hyperparameters are commonly used by the user to tweak their model and do experiments to find the best solution to their problem. In Foundations, hyperparameters objects are created by instantiating the `Hyperparameter` class and can be passed to stages returned by `create_stage()`. Their values must be set when running the stage. See an [example](../running_stages/#hyperparameter_example).

### Caching

Foundations is able to keep stage results in a cache so they can be re-used without having to run those stages again. This is useful for running multiple experiments when input parameters of some stages of the user's solution don't change among different runs, so their results are the same and don't require re-calculations.

### Job

A job in Foundations is a unit of work created when the user runs a stage. A job contains the stage being run and all stages it depends on. Jobs run in an execution environment that can be local or remote. When a stage is executed, the job object is created and deployed to the execution environment where it's picked up by Foundations' scheduler which is in charge of controlling it, tracking it and providing useful information about it to the user.
