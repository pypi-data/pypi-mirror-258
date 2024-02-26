#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkg_resources import parse_requirements
from setuptools import setup, find_packages

from gitlab_webhook_receiver import __version__


def load_requirements(filename):
    with open(filename, "r") as file:
        lines = (line.strip() for line in file)
        return [str(req) for req in parse_requirements(lines)]


setup(
    name="gitlab-webhook-receiver",
    version=__version__,
    url="https://github.com/dragonkid/gitlab-webhook-receiver",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "sh",
    ],
    entry_points={"console_scripts": ["gitlab-webhook-receiver = gitlab_webhook_receiver.receiver:main"]},
)
