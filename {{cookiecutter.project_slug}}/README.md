# {{cookiecutter.project_slug}} Analytics Project

This is a project for {{cookiecutter.feature_name}}

## Getting Started

These instructions will get you a copy of the application up and running on your local machine for development purposes.


### Prerequisites

- Python 3.8+
- `pipenv`

To set up dependencies

```shell
pip install pipenv 
pipenv sync -dev
pipenv run python setup.py install
```

### Running locally

To set up {{cookiecutter.feature_name}} project
```shell
```

To run the tests
```shell
pipenv run pytest

# run tests on different processes

pipenv run pytest --numprocesses 2
```

## Running the Data Validation Manually

It is possible to run a Jupyter Notebook with pipenv.

Steps:

Ensure you are not already running a pipenv virtual environment somewhere. Close down pycharm  I/ your IDE, then 
`deactivate`  and then `exit` (which will do nothing if you're not in a pipenv shell session anywhere).

Next, if you haven't, ensure ipykernel and the `[dev-packages]` packages have been added into your project, and activate your shell.

```shell
pipenv sync --dev
pipenv shell
```

Now you're ready to setup an ipykernel for this virtual env, and launch the notebook:

```shell
python -m ipykernel install --user --name=pipenv-{{cookiecutter.project_slug}}-notebook
jupyter notebook "research-notebooks/{{cookiecutter.feature_name}} Notebook.ipynb"
```

This will open the browser with your notebook.


The jupyter notebook should open with the correct `pipenv-{{cookiecutter.project_slug}}-notebook` "Kernel" (which will allow it run with all of the 
packages you have in the pipenv).

If this doesn't work, try changing the kernel in the notebook Menu bar.
Select `Kernel -> Change kernel -> pipenv-{{cookiecutter.project_slug}}-notebook`

You'll want to regenerate the notebook with the new Kernel, so `Kernel -> Restart & Run All`

## Built With

* [arrow](https://github.com/crsmithdev/arrow) - Better dates & times for Python
* [numpy](https://github.com/numpy/numpy) - The fundamental package for scientific computing with Python.
* [pandas](https://github.com/pandas-dev/pandas) - Flexible and powerful data analysis / manipulation library for Python 
* [scikit-learn](https://github.com/scikit-learn/scikit-learn) - Machine learning in Python
* [cassandra-driver](https://github.com/datastax/python-driver) - DataStax Python Driver for Apache Cassandra
* [python-json-logger](https://github.com/madzak/python-json-logger) - Json Formatter for the standard python logger
* [psycopg2](https://github.com/psycopg/psycopg2) - PostgreSQL database adapter for the Python programming language  
* [psutil](https://github.com/giampaolo/psutil) - Cross-platform lib for process and system monitoring in Python
* [python-dateutil](https://github.com/dateutil/dateutil) - Useful extensions to the standard Python datetime features
* [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) -  The Database Toolkit for Python 
* [prometheus_client](https://github.com/prometheus/client_python) - Prometheus instrumentation library for Python applications
* [pipenv](https://github.com/pypa/pipenv) - Python Development Workflow for Humans.
* [boto3](https://github.com/boto/boto3) - AWS SDK for Python  
* [scipy](https://github.com/scipy/scipy) - Scipy library main repository 


## Authors
