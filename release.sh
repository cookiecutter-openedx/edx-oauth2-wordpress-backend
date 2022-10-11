#!/bin/sh
#------------------------------------------------------------------------------
# written by: Lawrence McDaniel
#             https://lawrencemcdaniel.com
#
# date:       oct-2022
#
# usage:      a work in progress. build package and upload to PyPi.
#             https://pypi.org/project/wp-oauth-backend/
#             https://pypi.org/project/wp-oauth-backend-lpm0073/
#
# see: https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/
#------------------------------------------------------------------------------

python -m pip install --upgrade build
python3 -m build --sdist ./
python3 -m build --wheel ./

python3 -m pip install --upgrade twine
twine check dist/*

# PyPi test
twine upload --repository testpypi dist/*

# PyPi
twine upload dist/*
