import os
from setuptools import setup, find_packages
non_test_packages = [p for p in find_packages() if p.split('.')[-1] != 'tests']

requirements = []

setup(
    name='{{cookiecutter.project_slug}}',
    version='0.1',
    packages=non_test_packages,
    long_description=open('README.md', encoding="utf-8").read(),
    dependency_links=[],

)
