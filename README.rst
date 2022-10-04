OAuth2 Backend for WP Oauth
===========================

Overview
--------

A Python Social Auth backend for [WP OAuth](https://wp-oauth.com/), mostly used for Open edX but can be used elsewhere.
This package was originally cloned from https://github.com/appsembler/trinity-oauth-backend.

Open edX Setup
--------------

General Python/Django
~~~~~~~~~~~~~~~~~~~~~

include this repo in your project's requiremets.txt, or install it from the command line.

..  code-block:: shell

  cd path/to/your/project
  source path/to/venv/bin/activate
  pip install https://github.com/StepwiseMath/wp-oauth-backend

..  code-block:: yaml

  ADDL_INSTALLED_APPS:
  - "wp_oauth_backend"
  THIRD_PARTY_AUTH_BACKENDS:
  - "wp_oauth_backend.wp_oauth.StepwiseMathWPOAuth2"
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


Cookiecutter openedx_devops build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: shell

  - name: Add the wp-oauth-backend
    uses: openedx-actions/tutor-plugin-build-openedx-add-requirement@v1.0.0
    with:
      repository: wp-oauth-backend
      repository-organization: StepwiseMath
      repository-ref: main
      repository-token: ${{ secrets.PAT }}


Cookiecutter openedx_devops deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: shell

  tutor config save --set OPENEDX_WPOAUTH_BACKEND_BASE_URL="${{ secrets.WPOAUTH_BACKEND_BASE_URL }}" \
                    --set OPENEDX_WPOAUTH_BACKEND_CLIENT_ID="${{ secrets.WPOAUTH_BACKEND_CLIENT_ID }}" \
                    --set OPENEDX_WPOAUTH_BACKEND_CLIENT_SECRET="${{ secrets.WPOAUTH_BACKEND_CLIENT_SECRET }}"

WP Oauth Plugin Configuration
-----------------------------

This plugin enable your Open edX installation to authenticate against the WP Oauth plugin provider
in https://stepwisemath.ai/, configured as follows:

.. image:: doc/wp-oauth-config.png
  :width: 100%
  :alt: WP Oauth configuration page


Developer Notes
-------------

This package is structured so that it can be uploaded to PyPI and installed using pip or easyinstall.
More detail here: https://python-packaging.readthedocs.io/en/latest/minimal.html
