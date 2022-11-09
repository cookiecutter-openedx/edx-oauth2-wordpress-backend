Open edX OAuth2 Backend for Wordpress
=====================================
.. image:: https://img.shields.io/static/v1?label=pypi&style=flat-square&color=0475b6&message=edx-oauth2-wordpress-backend
  :alt: PyPi edx-oauth2-wordpress-backend
  :target: https://pypi.org/project/edx-oauth2-wordpress-backend/

.. image:: https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg
  :target: https://lawrencemcdaniel.com
  :alt: Hack.d Lawrence McDaniel

.. image:: https://img.shields.io/static/v1?logo=discourse&label=Discussions&style=flat-square&color=ff0080&message=OpenEdx
  :alt: Open edX Discussions
  :target: https://discuss.openedx.org/

.. image:: https://img.shields.io/static/v1?label=WP-Oauth&style=flat-square&color=1054ff&message=Server
  :alt: WP Oauth
  :target: https://wp-oauth.com/

|


Overview
--------

An Open edX oauth2 backend for `Wordpress <https://wordpress.org//>`_ `miniOrange OAuth / OpenID Connect Server <https://www.miniorange.com/>`_.

- `Python Social Auth custom backend implentation <https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html>`_
- `WP Oauth Wordpress Plugin Documentation <https://wp-oauth.com/docs/>`_

This is a strongly-typed implementation that leverages an in-depth knowledge of the WP Oauth return objects
to generate verbose, informative log data in `lms.log <./doc/lms.log>`_ that will help you to quickly get third party authentication
working on your Open edX installation.


Usage
-----

An example implementation for an Open edX installation named https://stepwisemath.ai/

1. add this package to your project's requiremets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

add this package to your project's requiremets.txt, or install it from the command line.

..  code-block:: shell

  pip install edx-oauth2-wordpress-backend

2. subclass WPOpenEdxOAuth2
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Subclass oauth2_wordpress.wp_oauth.WPOpenEdxOAuth2, and configure for your Wordpress oauth provider.

..  code-block:: python

  from oauth2_wordpress.wp_oauth import WPOpenEdxOAuth2


  class StepwiseMathWPOAuth2(WPOpenEdxOAuth2):

      # This defines the backend name and identifies it during the auth process.
      # The name is used in the URLs /login/<backend name> and /complete/<backend name>.
      #
      # This is the string value that will appear in the LMS Django Admin
      # Third Party Authentication / Provider Configuration (OAuth)
      # setup page drop-down box titled, "Backend name:", just above
      # the "Client ID:" and "Client Secret:" fields.
      name = "stepwisemath-oauth"

      # note: no slash at the end of the base url. Python Social Auth
      # might clean this up for you, but i'm not 100% certain of that.
      #
      # the following will create an authorization url of https://stepwisemath.ai/wp-json/moserver/authorize
      BASE_URL = "https://stepwisemath.ai"
      PATH = "wp-json/moserver/"
      AUTHORIZATION_ENDPOINT = "authorize"
      TOKEN_ENDPOINT = "token"
      USERINFO_ENDPOINT = "resource"


3. configure your Open edX lms application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: yaml

  ADDL_INSTALLED_APPS:
  - "oauth2_wordpress"
  THIRD_PARTY_AUTH_BACKENDS:
  - "oauth2_wordpress.wp_oauth.StepwiseMathWPOAuth2"
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
    - see: https://stepwisemath.ai/wp-admin/admin.php?page=mo_oauth_server_settings
  * - WPOAUTH_BACKEND_CLIENT_SECRET
    - see: https://stepwisemath.ai/wp-admin/admin.php?page=mo_oauth_server_settings
  * - SCOPE
    - basic email profile
  * - GRANT_TYPE
    - Authorization Code
  * - REDIRECT_URI
    - https://web.stepwisemath.ai/auth/complete/stepwisemath-oauth

4. Configure a new Oauth2 client from the lms Django Admin console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/lpm0073/edx-oauth2-wordpress-backend/main/doc/django-admin-1.png
  :width: 100%
  :alt: Open edX Django Admin Add Provider Configuration (OAuth)

.. image:: https://raw.githubusercontent.com/lpm0073/edx-oauth2-wordpress-backend/main/doc/django-admin-2.png
  :width: 100%
  :alt: Open edX Django Admin Add Provider Configuration (OAuth)


Cookiecutter openedx_devops deployment

..  code-block:: shell

  tutor config save --set OPENEDX_WPOAUTH_BACKEND_BASE_URL="${{ secrets.WPOAUTH_BACKEND_BASE_URL }}" \
                    --set OPENEDX_WPOAUTH_BACKEND_CLIENT_ID="${{ secrets.WPOAUTH_BACKEND_CLIENT_ID }}" \
                    --set OPENEDX_WPOAUTH_BACKEND_CLIENT_SECRET="${{ secrets.WPOAUTH_BACKEND_CLIENT_SECRET }}"

WP Oauth Plugin Configuration
-----------------------------

This plugin enables your Open edX installation to authenticate against the WP Oauth plugin provider
in your Wordpress web site, configured as follows:

.. image:: https://raw.githubusercontent.com/lpm0073/edx-oauth2-wordpress-backend/main/doc/miniorange-oauth-config.png
  :width: 100%
  :alt: miniOrange OAuth configuration page

Sample lms log output
---------------------


..  code-block:: shell

    2022-10-06 20:17:08,832 INFO 19 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/auth/login/stepwisemath-oauth/", "context": {"user_id": null, "path": "/auth/login/stepwisemath-oauth/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/login", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {\"auth_entry\": [\"login\"], \"next\": [\"/dashboard\"]}, \"POST\": {}}", "time": "2022-10-06T20:17:08.832684+00:00", "event_type": "/auth/login/stepwisemath-oauth/", "event_source": "server", "page": null}
    2022-10-06 20:17:09,230 INFO 19 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:216 - AUTHORIZATION_URL: https://stepwisemath.ai/oauth/authorize
    [pid: 19|app: 0|req: 2/19] 192.168.4.4 () {68 vars in 1889 bytes} [Thu Oct  6 20:17:08 2022] GET /auth/login/stepwisemath-oauth/?auth_entry=login&next=%2Fdashboard => generated 0 bytes in 430 msecs (HTTP/1.1 302) 9 headers in 922 bytes (1 switches on core 0)
    2022-10-06 20:17:38,485 INFO 7 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/auth/complete/stepwisemath-oauth/", "context": {"user_id": null, "path": "/auth/complete/stepwisemath-oauth/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://stepwisemath.ai/", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {\"redirect_state\": [\"pdbIKIcEbhjVr3Kon5VXUWWiy5kuX921\"], \"code\": [\"q0antmap4qfamd6pe24jh75pdprahpdiyitmut0o\"], \"state\": [\"pdbIKIcEbhjVr3Kon5VXUWWiy5kuX921\"], \"iframe\": [\"break\"]}, \"POST\": {}}", "time": "2022-10-06T20:17:38.484675+00:00", "event_type": "/auth/complete/stepwisemath-oauth/", "event_source": "server", "page": null}
    2022-10-06 20:17:38,496 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:223 - ACCESS_TOKEN_URL: https://stepwisemath.ai/oauth/token
    2022-10-06 20:17:40,197 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:230 - USER_QUERY: https://stepwisemath.ai/oauth/me
    2022-10-06 20:17:40,197 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:363 - user_data() url: https://stepwisemath.ai/oauth/me?access_token=jx2zql9fw2jx9s7tayik4ybfjrmuhb7m5csb1mtl
    2022-10-06 20:17:41,965 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:368 - user_data() response: {
        "ID": "7",
        "display_name": "Test McBugster",
        "user_email": "test@stepwisemath.ai",
        "user_login": "testaccount",
        "user_nicename": "testaccount",
        "user_registered": "2022-10-06 19:57:56",
        "user_roles": [
            "administrator"
        ],
        "user_status": "0"
    }
    2022-10-06 20:17:41,966 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:269 - get_user_details() received wp-oauth user data response json dict: {
        "ID": "7",
        "display_name": "Test McBugster",
        "user_email": "test@stepwisemath.ai",
        "user_login": "testaccount",
        "user_nicename": "testaccount",
        "user_registered": "2022-10-06 19:57:56",
        "user_roles": [
            "administrator"
        ],
        "user_status": "0"
    }
    2022-10-06 20:17:41,966 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:317 - get_user_details() processing response object
    2022-10-06 20:17:41,966 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:241 - user_details.setter: new value set {
        "date_joined": "2022-10-06 19:57:56",
        "email": "test@stepwisemath.ai",
        "first_name": "Test",
        "fullname": "Test McBugster",
        "id": 7,
        "is_staff": true,
        "is_superuser": true,
        "last_name": "McBugster",
        "refresh_token": "",
        "scope": "",
        "token_type": "",
        "user_status": "0",
        "username": "testaccount"
    }
    2022-10-06 20:17:41,967 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:345 - get_user_details() returning: {
        "date_joined": "2022-10-06 19:57:56",
        "email": "test@stepwisemath.ai",
        "first_name": "Test",
        "fullname": "Test McBugster",
        "id": 7,
        "is_staff": true,
        "is_superuser": true,
        "last_name": "McBugster",
        "refresh_token": "",
        "scope": "",
        "token_type": "",
        "user_status": "0",
        "username": "testaccount"
    }
    2022-10-06 20:17:41,972 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:269 - get_user_details() received extended get_user_details() return dict: {
        "access_token": "jx2zql9fw2jx9s7tayik4ybfjrmuhb7m5csb1mtl",
        "date_joined": "2022-10-06 19:57:56",
        "email": "test@stepwisemath.ai",
        "expires_in": 3600,
        "first_name": "Test",
        "fullname": "Test McBugster",
        "id": 7,
        "is_staff": true,
        "is_superuser": true,
        "last_name": "McBugster",
        "refresh_token": "",
        "scope": "",
        "token_type": "",
        "user_status": "0",
        "username": "testaccount"
    }
    2022-10-06 20:17:41,973 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:241 - user_details.setter: new value set {
        "access_token": "jx2zql9fw2jx9s7tayik4ybfjrmuhb7m5csb1mtl",
        "date_joined": "2022-10-06 19:57:56",
        "email": "test@stepwisemath.ai",
        "expires_in": 3600,
        "first_name": "Test",
        "fullname": "Test McBugster",
        "id": 7,
        "is_staff": true,
        "is_superuser": true,
        "last_name": "McBugster",
        "refresh_token": "",
        "scope": "",
        "token_type": "",
        "user_status": "0",
        "username": "testaccount"
    }
    2022-10-06 20:17:41,973 INFO 7 [oauth2_wordpress.wp_oauth] [user None] [ip 192.168.6.26] wp_oauth.py:290 - get_user_details() returning extended get_user_details() return dict: {
        "access_token": "jx2zql9fw2jx9s7tayik4ybfjrmuhb7m5csb1mtl",
        "date_joined": "2022-10-06 19:57:56",
        "email": "test@stepwisemath.ai",
        "expires_in": 3600,
        "first_name": "Test",
        "fullname": "Test McBugster",
        "id": 7,
        "is_staff": true,
        "is_superuser": true,
        "last_name": "McBugster",
        "refresh_token": "",
        "scope": "",
        "token_type": "",
        "user_status": "0",
        "username": "testaccount"
    }
    [pid: 7|app: 0|req: 2/20] 192.168.4.4 () {70 vars in 2136 bytes} [Thu Oct  6 20:17:38 2022] GET /auth/complete/stepwisemath-oauth/?redirect_state=pdbIKIcEbhjVr3Kon5VXUWWiy5kuX921&code=q0antmap4qfamd6pe24jh75pdprahpdiyitmut0o&state=pdbIKIcEbhjVr3Kon5VXUWWiy5kuX921&iframe=break => generated 0 bytes in 3549 msecs (HTTP/1.1 302) 9 headers in 612 bytes (1 switches on core 0)
    2022-10-06 20:17:42,211 INFO 19 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/register", "context": {"user_id": null, "path": "/register", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://stepwisemath.ai/", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {}}", "time": "2022-10-06T20:17:42.211436+00:00", "event_type": "/register", "event_source": "server", "page": null}
    [pid: 19|app: 0|req: 3/21] 192.168.4.4 () {70 vars in 1796 bytes} [Thu Oct  6 20:17:42 2022] GET /register => generated 37606 bytes in 177 msecs (HTTP/1.1 200) 8 headers in 600 bytes (1 switches on core 0)
    2022-10-06 20:17:42,527 INFO 7 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/stepwise/api/v1/configuration/prod", "context": {"user_id": null, "path": "/stepwise/api/v1/configuration/prod", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {}}", "time": "2022-10-06T20:17:42.527217+00:00", "event_type": "/stepwise/api/v1/configuration/prod", "event_source": "server", "page": null}
    [pid: 7|app: 0|req: 3/22] 192.168.4.4 () {68 vars in 1755 bytes} [Thu Oct  6 20:17:42 2022] GET /stepwise/api/v1/configuration/prod => generated 167 bytes in 41 msecs (HTTP/1.1 200) 6 headers in 189 bytes (1 switches on core 0)
    2022-10-06 20:17:42,617 INFO 19 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/api/user/v2/account/registration/", "context": {"user_id": null, "path": "/api/user/v2/account/registration/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {\"next\": [\"/dashboard\"], \"email\": [\"test@stepwisemath.ai\"], \"name\": [\"Test McBugster\"], \"username\": [\"testaccount\"], \"password\": \"********\", \"level_of_education\": [\"\"], \"gender\": [\"\"], \"year_of_birth\": [\"\"], \"mailing_address\": [\"\"], \"goals\": [\"\"], \"social_auth_provider\": [\"Stepwise\"], \"terms_of_service\": [\"true\"]}}", "time": "2022-10-06T20:17:42.616767+00:00", "event_type": "/api/user/v2/account/registration/", "event_source": "server", "page": null}
    2022-10-06 20:17:42,620 INFO 7 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/api/user/v1/validation/registration", "context": {"user_id": null, "path": "/api/user/v1/validation/registration", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {\"name\": [\"Test McBugster\"], \"username\": [\"testaccount\"], \"password\": \"********\", \"email\": [\"test@stepwisemath.ai\"], \"terms_of_service\": [\"false\"]}}", "time": "2022-10-06T20:17:42.619453+00:00", "event_type": "/api/user/v1/validation/registration", "event_source": "server", "page": null}
    [pid: 7|app: 0|req: 4/23] 192.168.4.4 () {74 vars in 1928 bytes} [Thu Oct  6 20:17:42 2022] POST /api/user/v1/validation/registration => generated 205 bytes in 85 msecs (HTTP/1.1 200) 8 headers in 282 bytes (1 switches on core 0)
    2022-10-06 20:17:42,719 INFO 7 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/api/user/v1/validation/registration", "context": {"user_id": null, "path": "/api/user/v1/validation/registration", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {\"name\": [\"Test McBugster\"], \"username\": [\"testaccount\"], \"password\": \"********\", \"email\": [\"test@stepwisemath.ai\"], \"terms_of_service\": [\"false\"]}}", "time": "2022-10-06T20:17:42.719504+00:00", "event_type": "/api/user/v1/validation/registration", "event_source": "server", "page": null}
    [pid: 7|app: 0|req: 5/24] 192.168.4.4 () {74 vars in 1928 bytes} [Thu Oct  6 20:17:42 2022] POST /api/user/v1/validation/registration => generated 205 bytes in 102 msecs (HTTP/1.1 200) 8 headers in 282 bytes (1 switches on core 0)
    2022-10-06 20:17:42,816 INFO 7 [tracking] [user None] [ip 192.168.6.26] logger.py:41 - {"name": "/api/user/v1/validation/registration", "context": {"user_id": null, "path": "/api/user/v1/validation/registration", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {\"name\": [\"Test McBugster\"], \"username\": [\"testaccount\"], \"password\": \"********\", \"email\": [\"test@stepwisemath.ai\"], \"terms_of_service\": [\"false\"]}}", "time": "2022-10-06T20:17:42.816042+00:00", "event_type": "/api/user/v1/validation/registration", "event_source": "server", "page": null}
    [pid: 7|app: 0|req: 6/25] 192.168.4.4 () {74 vars in 1928 bytes} [Thu Oct  6 20:17:42 2022] POST /api/user/v1/validation/registration => generated 205 bytes in 77 msecs (HTTP/1.1 200) 8 headers in 282 bytes (1 switches on core 0)
    2022-10-06 20:17:43,160 INFO 19 [audit] [user 53] [ip 192.168.6.26] models.py:2753 - Login success - user.id: 53
    2022-10-06 20:17:43,221 INFO 19 [tracking] [user 53] [ip 192.168.6.26] logger.py:41 - {"name": "edx.user.settings.changed", "context": {"user_id": null, "path": "/api/user/v2/account/registration/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": {"old": null, "new": "en", "truncated": [], "setting": "pref-lang", "user_id": 53, "table": "user_api_userpreference"}, "time": "2022-10-06T20:17:43.220899+00:00", "event_type": "edx.user.settings.changed", "event_source": "server", "page": null}
    2022-10-06 20:17:43,239 INFO 19 [tracking] [user 53] [ip 192.168.6.26] logger.py:41 - {"name": "edx.user.settings.changed", "context": {"user_id": null, "path": "/api/user/v2/account/registration/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "", "session": "a3f4ac2a5bf97f717f5745984059891b", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": {"old": false, "new": true, "truncated": [], "setting": "is_active", "user_id": 53, "table": "auth_user"}, "time": "2022-10-06T20:17:43.238965+00:00", "event_type": "edx.user.settings.changed", "event_source": "server", "page": null}
    /openedx/venv/lib/python3.8/site-packages/django/db/models/fields/__init__.py:1416: RuntimeWarning: DateTimeField Registration.activation_timestamp received a naive datetime (2022-10-06 20:17:43.246811) while time zone support is active.
      warnings.warn("DateTimeField %s received a naive datetime (%s)"
    2022-10-06 20:17:43,254 INFO 19 [common.djangoapps.student.models] [user 53] [ip 192.168.6.26] models.py:938 - User testaccount (test@stepwisemath.ai) account is successfully activated.
    2022-10-06 20:17:43,255 INFO 19 [openedx_events.tooling] [user 53] [ip 192.168.6.26] tooling.py:160 - Responses of the Open edX Event <org.openedx.learning.student.registration.completed.v1>:
    []
    2022-10-06 20:17:43,261 INFO 19 [audit] [user 53] [ip 192.168.6.26] register.py:295 - Login success on new account creation - testaccount
    [pid: 19|app: 0|req: 4/26] 192.168.4.4 () {74 vars in 1881 bytes} [Thu Oct  6 20:17:42 2022] POST /api/user/v2/account/registration/ => generated 79 bytes in 1145 msecs (HTTP/1.1 200) 15 headers in 3254 bytes (1 switches on core 0)
    2022-10-06 20:17:44,014 INFO 7 [tracking] [user 53] [ip 192.168.6.26] logger.py:41 - {"name": "/auth/complete/stepwisemath-oauth/", "context": {"user_id": 53, "path": "/auth/complete/stepwisemath-oauth/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "testaccount", "session": "4b87c052d7ba72c52f84c82737834d90", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {}}", "time": "2022-10-06T20:17:44.014681+00:00", "event_type": "/auth/complete/stepwisemath-oauth/", "event_source": "server", "page": null}
    /openedx/venv/lib/python3.8/site-packages/django/db/models/fields/__init__.py:1416: RuntimeWarning: DateTimeField User.date_joined received a naive datetime (2022-10-06 19:57:56) while time zone support is active.
      warnings.warn("DateTimeField %s received a naive datetime (%s)"
    2022-10-06 20:17:44,100 INFO 7 [tracking] [user 53] [ip 192.168.6.26] logger.py:41 - {"name": "edx.user.settings.changed", "context": {"user_id": 53, "path": "/auth/complete/stepwisemath-oauth/", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "testaccount", "session": "4b87c052d7ba72c52f84c82737834d90", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": {"old": "2022-10-06T20:17:42.674048+00:00", "new": "2022-10-06 19:57:56", "truncated": [], "setting": "date_joined", "user_id": 53, "table": "auth_user"}, "time": "2022-10-06T20:17:44.100229+00:00", "event_type": "edx.user.settings.changed", "event_source": "server", "page": null}
    [pid: 7|app: 0|req: 7/27] 192.168.4.4 () {66 vars in 3727 bytes} [Thu Oct  6 20:17:43 2022] GET /auth/complete/stepwisemath-oauth/? => generated 0 bytes in 150 msecs (HTTP/1.1 302) 10 headers in 721 bytes (1 switches on core 0)
    2022-10-06 20:17:44,375 INFO 19 [tracking] [user 53] [ip 192.168.6.26] logger.py:41 - {"name": "/dashboard", "context": {"user_id": 53, "path": "/dashboard", "course_id": "", "org_id": "", "enterprise_uuid": ""}, "username": "testaccount", "session": "4b87c052d7ba72c52f84c82737834d90", "ip": "192.168.6.26", "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", "host": "web.stepwisemath.ai", "referer": "https://web.stepwisemath.ai/register", "accept_language": "en-US,en;q=0.9,es-MX;q=0.8,es-US;q=0.7,es;q=0.6", "event": "{\"GET\": {}, \"POST\": {}}", "time": "2022-10-06T20:17:44.374973+00:00", "event_type": "/dashboard", "event_source": "server", "page": null}
