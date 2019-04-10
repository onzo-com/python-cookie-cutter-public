import logging
import os
import unittest

import pytest
from {{cookiecutter.project_slug}}.analytics.{{cookiecutter.feature_name}}.tests.postgresql_test_infrastructure import postgresqlTestCase


class TestPG(unittest.TestCase):

    @pytest.mark.skipif(os.uname().sysname == "Darwin", reason="Not running in a container")
    @postgresqlTestCase
    def test_check_connection(self, postgres):
        with postgres.cursor() as cursor:
            cursor.execute('SELECT version();')
            version = cursor.fetchone()[0]
            logging.info("DB version: {0}".format(version))
            expected = 'PostgreSQL 9.6.10 on x86_64-alpine-linux-musl, compiled by gcc (Alpine 6.3.0) 6.3.0, 64-bit'
            assert (version == expected)
