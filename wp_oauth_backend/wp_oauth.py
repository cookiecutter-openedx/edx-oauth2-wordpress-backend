"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           oct-2022

usage:          subclass of BaseOAuth2 Third Party Authtencation client to 
                handle the field mapping and data conversions between 
                the dict that WP Oauth returns versus the dict that Open edX 
                actually needs.
"""
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from social_core.backends.oauth import BaseOAuth2

from logging import getLogger
logger = getLogger(__name__)

VERBOSE_LOGGING = True
class StepwiseMathWPOAuth2(BaseOAuth2):
    """
    WP OAuth authentication backend customized for Open edX.
    see https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html
    """

    def __init__(self, strategy, redirect_uri=None):
        super().__init__(strategy, redirect_uri)

        if VERBOSE_LOGGING:
            logger.info('StepwiseMathWPOAuth2() -  ready.')

    # This defines the backend name and identifies it during the auth process. 
    # The name is used in the URLs /login/<backend name> and /complete/<backend name>.
    #
    # This is the string value that will appear in the LMS Django Admin
    # Third Party Authentication / Provider Configuration (OAuth)
    # setup page drop-down box titled, "Backend name:", just above
    # the "Client ID:" and "Client Secret:" fields.
    name = 'stepwisemath-oauth'

    # note: no slash at the end of the base url. Python Social Auth
    # might clean this up for you, but i'm not 100% certain of that.
    BASE_URL = "https://stepwisemath.ai"

    # The default key name where the user identification field is defined, it’s 
    # used in the auth process when some basic user data is returned. This Id 
    # is stored in the UserSocialAuth.uid field and this, together with the 
    # UserSocialAuth.provider field, is used to uniquely identify a user association.
    ID_KEY = 'id'

    # Flags the backend to enforce email validation during the pipeline 
    # (if the corresponding pipeline social_core.pipeline.mail.mail_validation was enabled).
    REQUIRES_EMAIL_VALIDATION = False

    # Some providers give nothing about the user but some basic data like the 
    # user Id or an email address. The default scope attribute is used to 
    # specify a default value for the scope argument to request those extra bits.
    DEFAULT_SCOPE = 'basic'

    # Specifying the method type required to retrieve your access token if it’s 
    # not the default GET request.
    ACCESS_TOKEN_METHOD = 'POST'    

    # require redirect domain to match the original initiating domain.
    SOCIAL_AUTH_SANITIZE_REDIRECTS = True

    # During the auth process some basic user data is returned by the provider 
    # or retrieved by the user_data() method which usually is used to call 
    # some API on the provider to retrieve it. This data will be stored in the 
    # UserSocialAuth.extra_data attribute, but to make it accessible under some 
    # common names on different providers, this attribute defines a list of 
    # tuples in the form (name, alias) where name is the key in the user data 
    # (which should be a dict instance) and alias is the name to store it on extra_data.
    EXTRA_DATA = [
            ('id', 'id'),
            ('is_superuser', 'is_superuser'),
            ('is_staff', 'is_staff'),
            ('date_joined', 'date_joined'),
        ]

    # the value of the scope separator is user-defined. Check the 
    # scopes field value for your oauth client in your wordpress host.
    # the wp-oauth default value for scopes is 'basic' but can be
    # changed to a list. example 'basic, email, profile'. This 
    # list can be delimited with commas, spaces, whatever.
    SCOPE_SEPARATOR = " "

    # private utility function. not part of psa.
    def _urlopen(self, url):
        return urlopen(url).read().decode("utf-8")

    # override Python Social Auth default end points
    # see https://wp-oauth.com/docs/general/endpoints/
    @property
    def AUTHORIZATION_URL(self) -> str:
        return f"{self.BASE_URL}/oauth/authorize"

    @property
    def ACCESS_TOKEN_URL(self) -> str:
        return f"{self.BASE_URL}/oauth/token"

    @property
    def USER_QUERY(self) -> str:
        return f"{self.BASE_URL}/oauth/me"

    # see https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html
    def get_user_details(self, response) -> dict:
        """Return user details from the WP account"""

        if type(response)==dict:
            if ('ID' not in response.keys()) or ('user_email' not in response.keys()):
                logger.info('get_user_details() -  response object lacks required keys. exiting.')
                return {}

        if VERBOSE_LOGGING:
            if not response:
                logger.info('get_user_details() -  response is missing. exiting.')
                return {}

            logger.info('get_user_details() -  start. response: {response}'.format(
                response=json.dumps(response, sort_keys=True, indent=4)
                ))

        # try to parse out the first and last names
        split_name = response.get('display_name', '').split()
        first_name = split_name[0] if len(split_name) > 0 else ''
        last_name = split_name[-1] if len(split_name) == 2 else ''

        # check for superuser / staff status
        user_roles = response.get('user_roles', [])        
        super_user = 'administrator' in user_roles
        is_staff = 'administrator' in user_roles

        user_details = {
            'id': int(response.get('ID'), 0),
            'username': response.get('user_email', ''),
            'wp_username': response.get('user_login', ''),
            'email': response.get('user_email', ''),
            'first_name': first_name,
            'last_name': last_name,
            'fullname': response.get('display_name', ''),
            'is_superuser': super_user,
            'is_staff': is_staff,
            'refresh_token': response.get('refresh_token', ''),
            'scope': response.get('scope', ''),
            'token_type': response.get('token_type', ''),
            'date_joined': response.get('user_registered', ''),
            'user_status': response.get('user_status', ''),
        }
        if VERBOSE_LOGGING:
            logger.info('get_user_details() -  complete. user_details: {user_details}'.format(
                user_details=json.dumps(user_details, sort_keys=True, indent=4)
                ))
        return user_details

    # implementation of user_data()
    # note that in the case of wp oauth, the response object returned by self.USER_QUERY
    # is the same as the response object passed to get_user_details().
    #
    # see https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html
    def user_data(self, access_token, *args, **kwargs) -> dict:
        """Loads user data from service"""

        url = f'{self.USER_QUERY}?' + urlencode({
            'access_token': access_token
        })

        if VERBOSE_LOGGING:
            logger.info("user_data() url: {url}".format(url=url))

        try:
            response = json.loads(self._urlopen(url))
            user_details = self.get_user_details(response)
            return user_details
        except ValueError as e:
            logger.error('user_data() {err}'.format(err=e))
            return None
