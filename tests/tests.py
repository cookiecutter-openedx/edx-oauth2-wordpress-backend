import json

# Opening JSON file
f = open("./data/get_user_details_extended.json")

# returns JSON object as
# a dictionary
response = json.load(f)


def is_valid_user_details(response) -> bool:
    """
    validate that the object passed is a dict containing at least the keys
    in qc_keys.
    """
    qc_keys = [
        "id",
        "date_joined",
        "email",
        "first_name",
        "fullname",
        "is_staff",
        "is_superuser",
        "last_name",
        "username",
    ]
    if all(key in response for key in qc_keys):
        return True
    return False


def is_wp_oauth_refresh_token_response(response) -> bool:
    """
    validate that the structure of the response contains the keys of
    a refresh token dict.
    """
    if not is_valid_user_details(response):
        return False
    qc_keys = ["access_token", "expires_in", "refresh_token", "scope", "token_type"]
    if all(key in response for key in qc_keys):
        return True
    return False


print("is_valid_user_details")
print(is_valid_user_details(response))

print("is_wp_oauth_refresh_token_response")
print(is_wp_oauth_refresh_token_response(response))
