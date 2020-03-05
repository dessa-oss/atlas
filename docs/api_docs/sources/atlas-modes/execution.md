<h1>Execution Mode</h1>
---

This mode is ideal for first time users of Atlas.
It is well suited for running single experiments at a time and incorporating the SDK into existing code to enable metadata tracking and experiment versioning.

### Creating a project
Now, let's create a project directory called `my_atlas_project` with a `main.py` inside, with the follow contents:

```python
# main.py

import foundations
print("Hello world!")
```

Let's run this script using `python main.py ` and observe what happens in the GUI.
We see that a new project called `my_atlas_project` has been created with a single *job* inside.    

![Job Details](../assets/images/my_atlas_project.png)

**This import statement is all that's needed to get started with experiment version control.**
Everytime you execute this script, a new Job UUID associated with that run will be generated and the project directory will be versioned and archived.

You can use this Job UUID to retrieve an archived version of the project directory as well as logs associated with the run.

In the next few sections, we'll walk through a simple model training exercise to demonstrate the experiment tracking and version control features that come out-of-the-box in Execution mode.

### Tracking hyper-parameters & metrics

Let's now import the MNIST dataset and train a simple logistic regression model to predict the digit. Modify your `main.py` to look like this:

```python
import foundations
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

print("Loading data...")
X, y= fetch_openml('mnist_784', version=1, return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

max_iter = 5
foundations.log_param("max_iter", max_iter)
model = LogisticRegression(solver='saga', multi_class='multinomial', max_iter=max_iter)

print("Training Model...")
model.fit(X_train, y_train)

print("Evaluating model...")
accuracy = model.score(X_test, y_test)*100

foundations.log_metric("Accuracy", accuracy.item())
print("Complete!")
```

Let's run this script again and take a look at the experiment in the GUI. We'll see a running job in the GUI which should complete after a few minutes. We'll also see the `max_iter` hyper-parameter logged as well as the `accuracy` metric logged once the job is complete.

![metrics](../assets/images/param_metric_logging.png)

We use the `(key, value)` syntax to log hyperparameters and metrics. Please refer to the SDK Reference for additional information on how to log hyper-parameters and metrics.

### Tagging experiments
Next, let's add tags to our experiment so we can easily differentiate between different classes of jobs. Let's run it for only 2 iterations in the interest of time.

```python
import foundations
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

print("Loading data...")
X, y= fetch_openml('mnist_784', version=1, return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

max_iter = 2
solver = 'saga'
foundations.log_param("max_iter", max_iter)
foundations.set_tag(solver, "Solver")
model = LogisticRegression(solver=solver, multi_class='multinomial', max_iter=max_iter)

print("Training Model...")
model.fit(X_train, y_train)

print("Evaluating model...")
accuracy = model.score(X_test, y_test)*100
foundations.log_metric("Accuracy", accuracy.item())
print("Complete!")
```

Now we'll see tags appear next to our jobs. Multiple tags can be added to experiments in the same way to quickly gain context on the experiment

![Tags](../assets/images/tags.png)

### Saving artifacts
Artifacts associated with experiments can include images, audio files, text files and python objects. Images & audio can be viewed directly in the GUI and all artifacts can be downloaded from the GUI by click on the job detail icon on the right hand side of the screen.

The artifact must first be saved to disk before saving it within Atlas. Let's save our trained model so it can be used later. The syntax is `save_artifact(filepath, key)`.

```python
import foundations
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

print("Loading data...")
X, y= fetch_openml('mnist_784', version=1, return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

max_iter = 2
solver = 'saga'
foundations.log_param("max_iter", max_iter)
foundations.set_tag(solver, "Solver")
model = LogisticRegression(solver=solver, multi_class='multinomial', max_iter=max_iter)

print("Training Model...")
model.fit(X_train, y_train)

print("Evaluating model...")
accuracy = model.score(X_test, y_test)*100
foundations.log_metric("Accuracy", accuracy.item())

print("Saving model...")
pickle.dump(model, open("model.pkl", "wb"))
foundations.save_artifact("model.pkl", "Model")

print("Complete!")
```

![Saved Artifact](../assets/images/saved_artifact.png)

### Retrieving job archives

To retrieve the archive for a job run in execution mode, navigate to the GUI and copy the Job ID for the job of interest.
Job archives are stored under the `job_data/archive/<job_id>/artifacts` folder in your Foundations home directory (default: `~/.foundations`).
This job archive is the state of the project working directory at the end of the job.

Scheduling mode allows for use of the CLI to retrieve job archives amongst several additional features.     
