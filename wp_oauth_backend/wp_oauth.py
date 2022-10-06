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
from logging import getLogger
from social_core.backends.oauth import BaseOAuth2
from django.contrib.auth import get_user_model


User = get_user_model()
logger = getLogger(__name__)

VERBOSE_LOGGING = True
class StepwiseMathWPOAuth2(BaseOAuth2):
    """
    WP OAuth authentication backend customized for Open edX.
    see https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html

    Notes:
    - Python Social Auth social_core and/or Open edX's third party authentication core
      are finicky about how the "properties" are implemented. Anything that actually
      declared as a Python class variable needs to remain a Python class variable. 
      DO NOT refactor these into formal Python properties as something upstream will
      break your code.

    - for some reason adding an __init__() def to this class also causes something
      upstream to break. If you try this then you'll get an error about a missing 
      positional argument, 'strategy'.
    """
    _user_details = None

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
    #
    # wp-oauth supports 4 scopes: basic, email, profile, openeid. 
    # we want the first three of these.
    # see https://wp-oauth.com/docs/how-to/adding-supported-scopes/
    DEFAULT_SCOPE = ['basic', 'profile', 'email']

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
        """
        ensure that url response object is utf-8 encoded.
        """
        return urlopen(url).read().decode("utf-8")

    def is_valid_user_details(self, response) -> bool:
        """
        validate that the object passed is a dict containing at least the keys 
        in qc_keys.
        """
        if not type(response) == dict: 
            logger.warning('is_valid_user_details() was expecting a dict but received an object of type: {type}'.format(
                type=type(response)
            ))
            return False
        qc_keys = ['id', 'date_joined', 'email', 'first_name', 'fullname', 'is_staff', 'is_superuser', 'last_name', 'username']
        if all(key in response for key in qc_keys): return True
        logger.warning('is_valid_user_details() received an invalid response: {response}'.format(
            response=json.dumps(response, sort_keys=True, indent=4)
        ))
        return False

    def is_wp_oauth_response(self, response) -> bool:
        """
        validate the structure of the response object from wp-oauth. it's 
        supposed to be a dict with at least the keys included in qc_keys.
        """
        if not type(response) == dict: 
            logger.warning('is_valid_user_details() was expecting a dict but received an object of type: {type}'.format(
                type=type(response)
            ))
            return False
        qc_keys = ['ID' 'display_name', 'user_email', 'user_login', 'user_roles']
        if all(key in response for key in qc_keys): return True
        logger.warning('is_wp_oauth_response() received an invalid response: {response}'.format(
            response=json.dumps(response, sort_keys=True, indent=4)
        ))
        return False

    def is_wp_oauth_extended_response(self, response) -> bool:
        """
        validate the structure of the extended response object from wp-oauth. it's 
        supposed to be a dict with at least the keys included in qc_keys.
        """
        if not self.is_valid_user_details(response): return False
        qc_keys = ['access_token' 'expires_in', 'refresh_token', 'scope', 'token_type']
        if all(key in response for key in qc_keys): return True
        return False
    # override Python Social Auth default end points.
    # see https://wp-oauth.com/docs/general/endpoints/
    #
    # Note that we're only implementing Python properties
    # so that we can include logging for diagnostic purposes.
    @property
    def AUTHORIZATION_URL(self) -> str:
        retval = f"{self.BASE_URL}/oauth/authorize"
        if VERBOSE_LOGGING:
            logger.info('AUTHORIZATION_URL: {url}'.format(url=retval))
        return retval

    @property
    def ACCESS_TOKEN_URL(self) -> str:
        retval = f"{self.BASE_URL}/oauth/token"
        if VERBOSE_LOGGING:
            logger.info('ACCESS_TOKEN_URL: {url}'.format(url=retval))
        return retval

    @property
    def USER_QUERY(self) -> str:
        retval = f"{self.BASE_URL}/oauth/me"
        if VERBOSE_LOGGING:
            logger.info('USER_QUERY: {url}'.format(url=retval))
        return retval

    @property
    def user_details(self) -> dict:
        return self._user_details

    @user_details.setter
    def user_details(self, value: dict):
        if self.is_valid_user_details(value):
            if VERBOSE_LOGGING:
                logger.info('user_details.setter: new value set {value}'.format(
                    value=json.dumps(value, sort_keys=True, indent=4)
                ))
            self._user_details = value
        else:
            logger.error('user_details.setter: tried to pass an invalid object {value}'.format(
                value=json.dumps(value, sort_keys=True, indent=4)
            ))

    # see https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html
    # Return user details from the Wordpress user account
    def get_user_details(self, response) -> dict:
        if not (self.is_valid_user_details(response) or self.is_wp_oauth_response(response)):
            logger.error('get_user_details() -  received an unrecognized response object. Cannot conitnue: {response}'.format(
                response=json.dumps(response, sort_keys=True, indent=4)
                ))
            # if we have cached results then we might be able to recover.
            return self.user_details

        if VERBOSE_LOGGING: logger.info('get_user_details() begin with response: {response}'.format(
            response=json.dumps(response, sort_keys=True, indent=4)
        ))
        # a def in the third_party_auth pipeline list calls get_user_details() after its already
        # been called once. i don't know why. but, it passes the original get_user_details() dict
        # enhanced with additional token-related keys. if we receive this modified dict then we 
        # should pass it along to the next defs in the pipeline.
        #
        # If most of the original keys (see dict definition below) exist in the response object
        # then we can assume that this is our case.
        if self.is_wp_oauth_extended_response(response):
            # -------------------------------------------------------------
            # expected use case #2: a potentially enhanced version of an original user_details dict.
            # -------------------------------------------------------------
            if VERBOSE_LOGGING:
                logger.info('get_user_details() -  detected an enhanced get_user_details() dict in the response: {response}'.format(
                    response=json.dumps(response, sort_keys=True, indent=4)
                    ))
            return response

        # at this point we've ruled out the possibility of the response object 
        # being a derivation of a user_details dict. So, it should therefore
        # conform to the structure of a wp-oauth dict. 
        if not self.is_wp_oauth_response(response):
            logger.warning('get_user_details() -  response object is not a valid wp-oauth object. Cannot continue. {response}'.format(
                response=json.dumps(response, sort_keys=True, indent=4)
            ))
            return self.user_details

        # -------------------------------------------------------------
        # expected use case #1: response object is a dict with all required keys.
        # -------------------------------------------------------------
        if VERBOSE_LOGGING:
            logger.info('get_user_details() -  start. response: {response}'.format(
                response=json.dumps(response, sort_keys=True, indent=4)
                ))

        # ---------------------------------------------------------------------
        # build and internally cache the get_user_details() dict
        # ---------------------------------------------------------------------

        # try to parse out the first and last names
        split_name = response.get('display_name', '').split()
        first_name = split_name[0] if len(split_name) > 0 else ''
        last_name = split_name[-1] if len(split_name) == 2 else ''

        # check for superuser / staff status
        user_roles = response.get('user_roles', [])        
        super_user = 'administrator' in user_roles
        is_staff = 'administrator' in user_roles

        self.user_details = {
            'id': int(response.get('ID'), 0),
            'username': response.get('user_login', ''),
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
            logger.info('get_user_details() -  finish. user_details: {user_details}'.format(
                user_details=json.dumps(self.user_details, sort_keys=True, indent=4)
                ))
        return self.user_details

    # Load user data from service url end point. Note that in the case of 
    # wp oauth, the response object returned by self.USER_QUERY
    # is the same as the response object passed to get_user_details().
    #
    # see https://python-social-auth.readthedocs.io/en/latest/backends/implementation.html
    def user_data(self, access_token, *args, **kwargs) -> dict:

        url = f'{self.USER_QUERY}?' + urlencode({
            'access_token': access_token
        })

        if VERBOSE_LOGGING:
            logger.info("user_data() url: {url}".format(url=url))

        try:
            response = json.loads(self._urlopen(url))
        except ValueError as e:
            logger.error('user_data() {err}'.format(err=e))
            return None

        if not self.is_valid_user_details(response):
            logger.error('user_data() response object is invalid: {response}'.format(
                response=json.dumps(self.user_details, sort_keys=True, indent=4)
            ))
            return self.user_details
        
        # refresh our internal user_details property after having validated
        # response from USER_QUERY
        self.get_user_details(response)

        # add syncronization of any data fields that get missed by the built-in
        # open edx third party authentication sync functionality.
        try:
            # this gets called just prior to account creation for
            # new users, hence, we need to catch DoesNotExist
            # exceptions.
            user=User.objects.get(username=self.user_details['username'])
        except User.DoesNotExist:
            return self.user_details

        if (user.is_superuser != self.user_details['is_superuser']) or (user.is_staff != self.user_details['is_staff']):
            user.is_superuser = self.user_details['is_superuser']
            user.is_staff = self.user_details['is_staff']
            user.save()
            logger.info('Updated the is_superuser/is_staff flags for user {username}'.format(username=user.username))

        if (user.first_name != self.user_details['first_name']) or (user.last_name != self.user_details['last_name']):
            user.first_name = self.user_details['first_name']
            user.last_name = self.user_details['last_name']
            user.save()
            logger.info('Updated first_name/last_name for user {username}'.format(username=user.username))

        return self.user_details
