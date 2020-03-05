# The Atlas GUI

### Introduction

![Overview page](assets/images/overview.png "Overview page")

Foundations Atlas helps you easily add record keeping into your modeling workflow — something essential in the modern-day modeling lifecycle.

Almost every piece of information can be retrieved and examined through the Foundations CLI, but our GUI gives you a better experience than working from a Terminal session does.

!!! note
    Although a refresh button is located on the page, the content per job is available to the GUI *immediately* after the
    line storing the information is run in your code. This means, among other things, that if you are saving a photo of your 
    training loss graph per epoch, you will see it live in the artifact viewer. Press "REFRESH TABLE" to see the changes.

---

### Project Directory

The project directory is a centralized location for all available projects that have been created within Atlas.
You can find your project here, under the same name as the job from which it was launched.

---

### Job Details page

This page shows all information on any job that has run under a given project.

A given job row will typically look like the following:

![Job detail row](assets/images/job-details-page-job-row.png "Job detail row")

#### Metrics and Parameters Graph

![Metrics and Parameters Graph](assets/images/parcoords-select.gif "Metrics and Parameters Graph")

You can quickly view all your job information in one glance in this interactive parallel coordinates graph. Each line represents a single job and each selected metric and parameter is its own axis.

You can select via the dropdown menus certain metrics and parameters that you wish you view.

![Metrics and Parameters Columns](assets/images/parcoords-column.gif "Metrics and Parameters Columns")

You can click and drag columns around to view the information in an organized manner. You can also select ranges of values to highlight by dragging across the axes.

#### Job Details

The leftmost section of the job information gives basic information about a specific run.

The **Job ID** is exactly as stated and allows us to retrieve information through the CLI and SDK. Clicking the icon beside
the string of characters will copy the ID to your clipboard.

The **status** can be in 1 of 4 states:
 
 1. Queued, a yellow circle
 
 2. Running, a green loading circle

 3. Completed, a green circle with a white check mark

 4. Error, a red circle with a white exclamation mark

!!! note 
    If you get an error state, you can check the logs of a job at any point using the `foundations get logs` CLI command.

**Launched** gives a recorded time of when the job launched.

**Duration** is how long the job ran for.

**User** this is the name you got from your administrator when you signed up for an Atlas account or your machines username if authentication is not available.

The **tags** section is really useful, this shows any tag that is attached to a given job. Tags are explained more in
the [SDK Reference](https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/sdk-reference/SDK/).

#### Parameters

Any parameters that you log within your code will be displayed here, with the key becoming the column name and value
becoming the value in the column.

Parameters consist of any input to your code or model that change how it runs.

If you launch a job with a new parameter that no other jobs have had before, a new column will appear
with that parameter. All jobs that do not log this parameter will have "*not available*" in this column.

!!! note 
    If there are too many columns, this section can be horizontally scrolled and can also be filtered.

#### Metrics

Any metrics that you log within your code will be displayed here, with the key becoming the column name and value
becoming the value in the column.

Metrics consist of any output of your code or model that describes how it ran.

If you launch a job with a new metric that no other job has had before, a new column will appear
with that metric. All jobs that do not log this metric will have "*not available*" in this column.

!!! note
    If there are too many columns, this section can be horizontally scrolled and can also be filtered.

#### Send to Tensorboard

Atlas offers the ability for the user to log files that Tensorboard would normally read, place them in a stored location,
and then — seamlessly in the GUI — open a Tensorboard server for those stored files.

To use this feature, make sure that your code uses the `set_tensorboard_logdir()` SDK command. Any job that uses this function will
automatically be tagged with the Tensorboard logo. Then, simply select the checkbox beside the job (or jobs) that you
want to see in Tensorboard and click the "SEND TO TENSORBOARD" button.

*A new tab will open in your browser with a Tensorboard server that has each job as a selectable run in the bottom left.*

!!! note
    If the jobs don't appear as expected, try refreshing your browser page.

#### Filtering columns

If you log very many parameters or metrics, you may find that you would like to
filter out certain columns, to make it easy to find the results you need. You can use the "Filter Columns" dropdown menu to 
restrict the columns that are displayed to only those that you wish to focus on.

---

### Job Details modal

At the far right of each job row is a job details icon that opens a modal that will give information
about a specific job that doesn't really fit into a table. 

#### Tags

Here we can see all of the tags attached to a specific job, and even interact with them. Adding and removing
tags after a job has completed can be really useful for more precise record keeping.

#### Artifacts

By saving files in your code using, you can view and retrieve these files through the GUI.

If you log a photo or an audio file, you can interact with it on this page.

---

### Project Overview page

This page gives you a high-level glance of the project to keep track of how your experiments are proceeding, along the 
lines of a scientific notebook.

#### The Graph

This graph plots a given metric from all jobs in a project over time giving you a quick glimpse into how your 
experimentation has been going throughout a projects life.

Hovering over a specific data point on the graph will show you the job id that generated that piece of information. This
can be helpful to track down which jobs to dive deeper into based on their metrics relative to other jobs. 

You will also see a dropdown selector in the top right of the graph section where you can select which metric you would
like to see.

#### Comments

This section of the Overview page lets you keep notes as your project evolves. 

!!! note
    If you are running Atlas in a shared environment, leaving notes for other data scientists, so they know what is going on, will help you collaborate.

#### Overview Markdown

This is a full-service markdown editor, for keeping more detailed documentation on a project. 

Documentation is key to a successful project!