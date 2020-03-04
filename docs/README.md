# Readthedocs and branches

We host our documentation on [readthedocs](https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/). We have configured readthedocs to compile different versions based on branches. Correspondingly we will be maintaining a branch per minor version. In addition, the master branch is the "latest" version shown in readthedocs.

## What this means for docs developers ##

Please make sure your changes are pushed to all relevant branches.

# How to add a page #

Add a new entry to the relevant part of the tree in the `nav` section in `mkdocs.yml`. The path to provide is relative to this repo's `atlas-ce-docs/docs/api_docs/sources` directory, which should point to any new pages that you intend to add. The pages must be in markdown.

# How to run locally

Install the `mkdocs` python package and you can then run `mkdocs serve` in the root of this project. This will serve the pages to test locally at [http://localhost:8000/](http://localhost:8000/).

# How to compile #
You must have admin access to our [readthedocs site](https://readthedocs.com/projects/dessa-atlas-community-docs/) in order to build the docs from the repo.
