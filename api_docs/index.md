# Foundations User API

To help use Foundations, we have API documentation that explains the possible classes and functions, and their signatures, that are available to Foundations users.

This documentation is auto-generated using `/api_docs/autogen.py`. We define files in `autogen.py`, which then goes through the defined files, looks at the class and function documentation snippets in each file, and outputs markdown files.

We then use [mkdocs.org](https://mkdocs.org) to take the markdown files and serve them in a webpage locally.

Configuration for documentation can be found in `mkdocs.yml`.

## How to add a new file to the docs

In `mkdocs.yml` you'll need to specify the title of the page, and a corresponding markdown file.

In `autogen.py` you'll then need to add the new file to the `PAGES` list. This is also where you list the class and functions that will be looped through to get their documentation snippets.

To see any changes you'll need to run `python autogen.py` to regenerate the markdown files with changes.

## Running documentation site locally

To run the API documentation site locally, inside `/api_docs` you can run:

- `python autogen.py` (will build and populate all necessary markdown files)
- `mkdocs serve` (will serve the documentation site to http://localhost:8000/)

An alternative to using `serve`, you can build a static version of the documentation site using `mkdocs build`. This will create a `/site` directory with a static version of the site built that you can access by opening `index.html`.


## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

