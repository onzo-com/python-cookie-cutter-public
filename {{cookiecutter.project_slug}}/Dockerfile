FROM dockerfilepath:3.8.3.8

ENV PATH="${PATH}:/root/.local/bin"
# Following env vars required for pipenv
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -eux \
    && apt-get --allow-releaseinfo-change update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && pip3 install --user --no-cache-dir pipenv \
    && rm -rf /var/lib/apt/lists/ \
    && : # last line

COPY . /app

WORKDIR /app

RUN set -eux \
    && pipenv sync \
    && pipenv run python3 setup.py install \
    && pipenv --clear \
    && : # last line

ENTRYPOINT [ "{{cookiecutter.feature_name}}", "run", "python3", "-m", "{{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}" ]
