# Cookiecutter Analytics Project

This repo is designed for a data science team to clone using cookiecutter to create a new analytics project from scratch with everything they need to get started including: 
* Pipenv
* IPython notebooks/ Jupyter Notebooks
* Postgres test infrastructure.

Relates to technical blog post: https://medium.com/onzo-tech/a-tool-all-python-developers-should-be-using-5d547bfb45b7

## Getting Started

These instructions will get you a copy of the application up and running on your local machine for development purposes.


### Prerequisites

- `cookiecutter`
- Python 3.8+
- `pipenv`

### Running locally

To set up cookiecutter project

```shell
brew install cookiecutter (see https://cookiecutter.readthedocs.io/en/latest/installation.html if you are not on MAC OS X)
cd <path where you want the new project>
cookiecutter https://github.com/onzo-com/python-cookie-cutter-public.git

create the name of your project directory e.g 'project_cookiecutter'
create the name of the feature directory e.g. 'feature_name'
create the name of the class feature (PEP8) e.g 'FeatureName' (will be used to create the template feature class and unit tests) 
```
You should now be able to open your new project in the IDE of your choice 

#### Once you have completed cookiecutter please read the README located in your new project for pre-requisites and local development


## Authors

Here is a list of [contributors](https://github.com/onzo-com/python-cookie-cutter-public/graphs/contributors) who participated
in this project.
