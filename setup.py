#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W6005,W6100

import os
import io
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "oauth2_wordpress", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split("#")[0].strip()
            for line in open(path).readlines()
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.
    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return not (
        line == ""
        or line.startswith("-c")
        or line.startswith("-r")
        or line.startswith("#")
        or line.startswith("-e")
        or line.startswith("git+")
    )


README = load_readme()
ABOUT = load_about()
VERSION = ABOUT["__version__"]

setup(
    name="edx-oauth2-wordpress-backend",
    version=VERSION,
    description=(
        "An OAuth backend for the WP OAuth Wordpress Plugin, "
        "that is customized for use in Open edX installations."
    ),
    long_description=README,
    author="Lawrence McDaniel, lpm0073@gmail.com",
    author_email="lpm0073@gmail.com",
    url="https://github.com/StepwiseMath/edx-oauth2-wordpress-backend",
    project_urls={
        "Code": "https://github.com/StepwiseMath/edx-oauth2-wordpress-backend",
        "Issue tracker": "https://github.com/StepwiseMath/edx-oauth2-wordpress-backend/issues",
        "Community": "https://stepwisemath.ai",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.html"]},  # include any templates found in this repo.
    zip_safe=False,
    keywords="Open edX, oauth, Wordpress",
    python_requires=">=3.7",
    install_requires=load_requirements("requirements/stable-psa.txt"),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
