from .wp_oauth import WPOpenEdxOAuth2


class StepwiseMathWPOAuth2(WPOpenEdxOAuth2):

    # This defines the backend name and identifies it during the auth process.
    # The name is used in the URLs /login/<backend name> and /complete/<backend name>.
    #
    # This is the string value that will appear in the LMS Django Admin
    # Third Party Authentication / Provider Configuration (OAuth)
    # setup page drop-down box titled, "Backend name:", just above
    # the "Client ID:" and "Client Secret:" fields.
    name = "swtest-oauth"

    # note: no slash at the end of the base url. Python Social Auth
    # might clean this up for you, but i'm not 100% certain of that.
    BASE_URL = "https://stepwisemath.ai"
