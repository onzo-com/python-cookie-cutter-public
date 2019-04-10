FROM dockerfilepath:latest
RUN apt-get update && apt-get -y install libpq-dev && pip3 install --user pipenv
ENV PATH="${PATH}:/root/.local/bin"
# Following env vars required for pipenv
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
COPY ../README.md setup.py Pipfile Pipfile.lock /app/
WORKDIR /app
RUN pipenv install && pipenv run python3 setup.py install
COPY . /app
ENTRYPOINT [ "{{cookiecutter.feature_name}}", "run", "python3", "-m", "{{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}" ]
