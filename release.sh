#!/bin/sh
#------------------------------------------------------------------------------
# written by: Lawrence McDaniel
#             https://lawrencemcdaniel.com
#
# date:       oct-2022
#
# usage:      a work in progress. build package and upload to PyPi.
#------------------------------------------------------------------------------

python -m pip install --upgrade build
python3 -m build --sdist ./ 
python3 -m build --wheel ./

python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
