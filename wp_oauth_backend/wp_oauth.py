import json
from urllib.parse import urlencode
from urllib.request import urlopen
from social_core.backends.oauth import BaseOAuth2

from logging import getLogger
logger = getLogger(__name__)


class WPOAuth2(BaseOAuth2):
    """WP OAuth authentication backend"""

    name = 'wp-oauth'

    # https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html
    SOCIAL_AUTH_SANITIZE_REDIRECTS = True       # for redirect domain to exactly match the initiating domain.
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    BASE_URL = "https://stepwisemath.ai"

    @property
    def base_url(self) -> str:
        return self.BASE_URL

    @property
    def AUTHORIZATION_URL(self) -> str:
        return f"{self.base_url}/oauth/authorize"

    @property
    def ACCESS_TOKEN_URL(self) -> str:
        return f"{self.base_url}/oauth/token"

    @property
    def EXTRA_DATA(self) -> list:
        return [
            ('id', 'id'),
            ('username', 'username'),
            ('email', 'email'),
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
            ('fullname', 'fullname'),
            ('is_superuser', 'is_superuser'),
            ('is_staff', 'is_staff'),
            ('date_joined', 'date_joined'),
        ]

    @property
    def USER_QUERY(self) -> str:
        return f"{self.base_url}/oauth/me"

    def get_user_details(self, response) -> dict:
        """Return user details from the WP account"""

        # try to parse out the first and last names
        split_name = response.get('display_name', '').split()
        first_name = split_name[0] if len(split_name) > 0 else ''
        last_name = split_name[-1] if len(split_name) == 2 else ''

        # check for superuser / staff status
        user_roles = response.get('user_roles', [])        
        super_user = 'administrator' in user_roles

        # create a unique but repeatable username
        username = response.get('user_login') + '_' + response.get('ID')

        user_details = {
            'id': int(response.get('ID')),
            'username': username,
            'email': response.get('user_email'),
            'first_name': first_name,
            'last_name': last_name,
            'fullname': response.get('display_name'),
            'is_superuser': super_user,
            'is_staff': super_user,
            'refresh_token': response.get('refresh_token'),
            'scope': response.get('scope'),
            'token_type': response.get('token_type'),
            'date_joined': response.get('user_registered'),
            'user_status': response.get('user_status'),
        }
        logger.info('get_user_details() -  user_details: {user_details}'.format(
            user_details=json.dumps(user_details, sort_keys=True, indent=4)
            ))
        return user_details

    def user_data(self, access_token, *args, **kwargs) -> dict:
        """Loads user data from service"""

        url = f'{self.USER_QUERY}?' + urlencode({
            'access_token': access_token
        })

        logger.info("user_data() url: {url}".format(url=url))

        try:
            response = json.loads(self.urlopen(url))
            user_details = self.get_user_details(response)
            return user_details
        except ValueError as e:
            logger.error('user_data() did not work: {err}'.format(err=e))
            return None

    def urlopen(self, url):
        return urlopen(url).read().decode("utf-8")

    # def get_user_id(self, details, response):
    #     return details['id']

    # def get_username(self, strategy, details, backend, user=None, *args, **kwargs):
    #     return details['username']
