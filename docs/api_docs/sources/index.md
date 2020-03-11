# Foundations Atlas

<p align="center">
  <img src="assets/images/dessa-square-logo.png">
</p>

<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>

<div align="center">
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/dessa-research/atlas" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star dessa-research/atlas on GitHub">Star</a>

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/dessa-research/atlas/fork" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-repo-forked" data-size="large" data-show-count="true" aria-label="Fork dessa-research/atlas on GitHub">Fork</a>

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/dessa-research" data-color-scheme="no-preference: light; light: light; dark: dark;" data-size="large" data-show-count="true" aria-label="Follow @dessa-research on GitHub">Follow @dessa-research</a>

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/dessa-research/atlas/subscription" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-eye" data-size="large" data-show-count="true" aria-label="Watch dessa-research/atlas on GitHub">Watch</a>

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/dessa-research/atlas/issues" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-issue-opened" data-size="large" data-show-count="true" aria-label="Issue dessa-research/atlas on GitHub">Issue</a>
</div>

## Atlas Documentation 

Atlas is a flexible Machine Learning platform that consists of a Python SDK, CLI, GUI & Scheduler to help Machine Learning Engineering teams dramatically reduce the model development time & reduce effort in managing infrastructure.

Atlas is a subset of *Foundations* which is a group of tools we have built for Machine Learning Engineers. 

![Platform Support](https://img.shields.io/badge/Platforms-osx%20%7C%20linux%20%7C%20windows-lightgrey "platform")
![Python Support](https://img.shields.io/badge/Python-%3E3.6-brightgreen "python")
![Downloads](https://img.shields.io/badge/Downloads-2000+-brightgreen "downloads")

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
  <iframe src="https://www.youtube.com/embed/YnwtO48UYAU?start=2" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

### BETA Note

Atlas has evolved quite a lot throughout our history. The latest open-source version of Atlas includes a lot of architectural and design changes. 

**This version is currently in BETA.**

### Here are some of the core features:

**Experiment Management & Tracking:**
<br>Tag experiments and easily track hyperparameters, metrics, and artifacts such as images, GIFs, and audio clips in a web-based GUI to track the performance of your models

![GUI](https://static.wixstatic.com/media/29a4f1_c8d1a4f9ab1941ab9ade5e934cf8b149~mv2.png/v1/fill/w_1440,h_1024/tumour.png "Artifact GUI")

**Job queuing & scheduling:** <br>Launch and queue thousands of experiment variations to fully utilize your system resources

![GUI](https://static.wixstatic.com/media/29a4f1_ffb0c04ef79843e79dbf2b1fa33a70c4~mv2.png/v1/fill/w_1440,h_1024/Time%20series%20forecast.png "GUI")

**Collaboration & Bookkeeping:** <br>Keep a journal of thoughts, ideas, and comments on projects

**Reproducibility:** <br>
Maintain an audit trail of every single experiment you run, complete with code and any saved items

**Authentication & other integrations:** <br>
Collaborate across your team by seting up Atlas on a cluster and aproviding user access controls via [KeyCloak integration](atlas-modes/authentication.md).

Slice and dice your models from the GUI via the [Tensorboard](gui.md) integration.

## How does Atlas Work?
Atlas consists of the following core modules:

* [GUI](gui.md) - A Dockerized web application to view job status for various projects.  
* Foundations [SDK](sdk-reference/SDK.md) & [CLI](cli.md) - A programmatic and command-line interfaces for Atlas.
* [Local Scheduler](atlas-modes/scheduling.md) - A scheduler which is used for job orchestration and management.

Here is an example workflow: 

1. Install Atlas on your machine or on the Cloud 
2. Use the SDK to log various metrics, hyperparameters or use the `submit` SDK command to automate submission of jobs for e.g:
```python
# main.py

import foundations 

foundations.log_metrics('accuracy', acc)
foundations.log_param('batch_size', 64)

foundations.save_artifact('loss_graph', loss_plt)

foundations.submit(scheduler_config="scheduler"
                    command=["main.py"],
                    num_gpus=1,
                    stream_job_logs=False)
```
3. Use the Foundations CLI to submit your jobs to your local or remote machine (or cluster).
```bash
foundations submit my_aws_scheduler_instance . main.py --num-gpus=3
```
4. Atlas packages your code into a container, reviews resources available, schedules and executes your job and displays the results on the [GUI](gui.md).  

## Contribute to Atlas
Atlas is open-source (Apache 2.0) and we welcome all levels of contributors!

To contribute to Atlas, get started on our [Github](www.github.com/dessa-research/atlas).

## Join the community 

Want to contribute to Atlas? or just want to get in touch with Atlas users and Dessa Deep Learning Engineers? Join our community Slack [here](https://join.slack.com/t/dessa-community/shared_invite/enQtNzY5ODkxOTc3OTkwLTk4MTg5NmNkOTQ5OWVjNjk2YzY0OWJlNDkwNDlhY2NmNTQzNmRmYjkxNzc2N2JiOTYxZGVkMmFiMjRhYThiYzM). 

Prefer discussing over e-mail? Send us a message [here](https://dessa.com/contact/).

## License

We ❤️ open source, Atlas is licensed using the [Apache 2.0 License](../../../LICENSE.txt). 

```
Copyright 2015-2020 Square, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

© 2020 Square, Inc. ATLAS, DESSA, the Dessa Logo, and others are trademarks of Square, Inc. All third party names and trademarks are properties of their respective owners and are used for identification purposes only.