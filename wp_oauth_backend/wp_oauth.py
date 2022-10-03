import json
from urllib.parse import urlencode
from urllib.request import urlopen
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings

from logging import getLogger
logger = getLogger(__name__)


class WPOAuth2(BaseOAuth2):

    """WP OAuth authentication backend"""
    name = 'wp-oauth'
    SOCIAL_AUTH_SANITIZE_REDIRECTS = False
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = []
    SCOPE_SEPARATOR = ','

    @property
    def base_url(self):
        return settings.WPOAUTH_BACKEND_BASE_URL

    @property
    def CLIENT_ID(self):
        return settings.WPOAUTH_BACKEND_CLIENT_ID

    @property
    def CLIENT_SECRET(self):
        return settings.WPOAUTH_BACKEND_CLIENT_SECRET

    @property
    def AUTHORIZATION_URL(self) -> str:
        return f"{self.base_url}/oauth/authorize"

    @property
    def ACCESS_TOKEN_URL(self) -> str:
        return f"{self.base_url}/oauth/token"

    @property
    def USER_QUERY(self) -> str:
        return f"{self.base_url}/oauth/me"

    def get_user_details(self, response):
        """Return user details from the WP account"""
        user_details = {
            'id': int(response.get('ID')),
            'username': response.get('user_login'),
            'email': response.get('user_email'),
            'fullname': response.get('display_name'),
        }
        logger.info('get_user_details() -  {}'.format(user_details))
        return user_details

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = f'{self.USER_QUERY}?' + urlencode({
            'access_token': access_token
        })

        try:
            return json.loads(self.urlopen(url))
        except ValueError:
            return None

    def urlopen(self, url):
        return urlopen(url).read().decode("utf-8")

    def get_user_id(self, details, response):
        return details['id']

    def get_username(self, strategy, details, backend, user=None, *args, **kwargs):
        return details['username']

    def get_key_and_secret(self):
        return (self.CLIENT_ID, self.CLIENT_SECRET)
