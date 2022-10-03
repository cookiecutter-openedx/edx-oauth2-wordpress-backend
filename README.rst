OAuth2 Backend for stepwisemath.ai
==================================

Overview
--------

A Python Social Auth backend for WP OAuth, mostly used for Open edX but can be used elsewhere.
This package was originally cloned from https://github.com/appsembler/trinity-oauth-backend.

This package is structured so that it can be uploaded to PyPI and installed using pip or easyinstall.
More detail here: https://python-packaging.readthedocs.io/en/latest/minimal.html

Setup
-----

General Python/Django
~~~~~~~~~~~~~~~~~~~~~

include this repo in your project's requiremets.txt, or install it from the command line.

..  code-block:: bash
    :caption: Python/Django installation
    cd path/to/your/project
    source path/to/venv/bin/activate
    pip install https://github.com/StepwiseMath/stepwisemath-oauth-backend

..  code-block:: yaml
    :caption: lms.envs.tutor.production.py
    ADDL_INSTALLED_APPS:
    - "wp_oauth_backend"
    THIRD_PARTY_AUTH_BACKENDS:
    - "stepwisemath_oauth_backend.wp_oauth.WPOAuth2"
    ENABLE_REQUIRE_THIRD_PARTY_AUTH: true

add these settings to django.conf:

.. list-table:: WP Oauth setup
  :widths: 50 100
  :header-rows: 1

  * - Key
    - Value
  * - WPOAUTH_BACKEND_BASE_URL
    - https://stepwisemath.ai
  * - WPOAUTH_BACKEND_CLIENT_ID
    - see: https://stepwisemath.ai/wp-admin/admin.php?page=wo_manage_clients
  * - WPOAUTH_BACKEND_CLIENT_SECRET
    - see: https://stepwisemath.ai/wp-admin/admin.php?page=wo_manage_clients


Cookiecutter openedx_devops
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. include this repository in your Build additional requirements
2. 

Developer Notes
-------------