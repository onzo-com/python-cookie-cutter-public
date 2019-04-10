import unittest
import logging

class Test{{cookiecutter.class_feature_name}}(unittest.TestCase):

    def test_{{cookiecutter.feature_name}}(self):

        logging.debug("This a template test for {{cookiecutter.project_slug}}")
        assert True