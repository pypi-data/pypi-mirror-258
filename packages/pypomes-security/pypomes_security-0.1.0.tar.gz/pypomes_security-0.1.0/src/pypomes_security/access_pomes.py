import requests
import sys
from datetime import datetime, timedelta
from logging import Logger
from pypomes_core import (
    APP_PREFIX, TIMEZONE_LOCAL,
    env_get_str, exc_format
)
from requests import Response
from typing import Final

SECURITY_TAG_USER_ID: Final[str] = env_get_str(f"{APP_PREFIX}_SECURITY_TAG_USER_ID")
SECURITY_TAG_USER_PWD: Final[str] = env_get_str(f"{APP_PREFIX}_SECURITY_TAG_USER_PWD")
SECURITY_URL_GET_TOKEN: Final[str] = env_get_str(f"{APP_PREFIX}_SECURITY_URL_GET_TOKEN")
SECURITY_USER_ID: Final[str] = env_get_str(f"{APP_PREFIX}_S,ECURITY_USER_ID")
SECURITY_USER_PWD: Final[str] = env_get_str(f"{APP_PREFIX}_SECURITY_USER_PWD")


def access_get_token(errors: list[str],
                     service_url: str = SECURITY_URL_GET_TOKEN,
                     user_id: str = SECURITY_TAG_USER_ID,
                     user_pwd: str = SECURITY_TAG_USER_PWD,
                     key_user_id: str = SECURITY_TAG_USER_ID,
                     key_user_pwd: str = SECURITY_TAG_USER_PWD,
                     timeout: int | None = None, logger: Logger = None) -> str:
    """
    Obtain and return an access token for further interaction with a protected resource.

    The current token is inspected to determine whether its expiration timestamp requires
    it to be refreshed.

    :param errors: incidental error messages
    :param timeout: timeout, in seconds (defaults to HTTP_POST_TIMEOUT - use None to omit)
    :param service_url: request URL for the access token
    :param user_id: id of user in request
    :param user_pwd: password of user in request
    :param key_user_id: key for sending user id in request
    :param key_user_pwd: key for sending user password in request
    :param logger: optional logger to log the operation with
    :return: the access token
    """
    # inicialize the return variable
    result: str | None = None

    # obtain the current access token timestamp
    token_timestamp: datetime = __get_expiration_timestamp(service_url)

    # establish the current date and time
    just_now: datetime = datetime.now(TIMEZONE_LOCAL)
    err_msg: str | None = None

    # is the current token still valid ?
    if just_now < token_timestamp:
        # yes, return it
        result = __access_tokens.get(service_url).get("access_token")
    else:
        # no, retrieve a new one
        payload: dict = {
            key_user_id: user_id,
            key_user_pwd: user_pwd
        }

        # send the REST request
        if logger:
            logger.info(f"Sending REST request to {service_url}: {payload}")
        try:
            # return data:
            # {
            #   "access_token": <token>,
            #   "expires_in": <seconds-to-expiration>
            # }
            response: Response = requests.post(
                url=service_url,
                json=payload,
                timeout=timeout
            )
            reply: dict | str
            token: str | None = None
            # was the request successful ?
            if response.status_code in [200, 201, 202]:
                # yes, retrieve the access token returned
                reply = response.json()
                token = reply.get("access_token")
                if logger:
                    logger.info(f"Access token obtained: {reply}")
            else:
                # no, retrieve the reason for the failure
                reply = response.reason

            # was the access token retrieved ?
            if token is not None and len(token) > 0:
                # yes, proceed
                url_token_data: dict = __access_tokens.get(service_url)
                url_token_data["access_token"] = token
                duration: int = reply.get("expires_in")
                url_token_data["expires_in"] = just_now + timedelta(seconds=duration)
                result = token
            else:
                # no, report the problem
                err_msg = f"Unable to obtain access token: {reply}"
        except Exception as e:
            # the operation raised an exception
            err_msg = f"Error obtaining access token: {exc_format(e, sys.exc_info())}"

    if err_msg:
        if logger:
            logger.error(err_msg)
        errors.append(err_msg)

    return result


# initial data for <access_url> in '__access_tokens':
# {
#   <access_url> = {
#     "access_token": None,
#     "expires_in": datetime(year=2000,
#                            month=1,
#                            day=1,
#                            tzinfo=TIMEZONE_LOCAL)
#   },
#   ...
# }
__access_tokens: dict = {}


def __get_expiration_timestamp(service_url: str) -> datetime:

    # obtain the data for the given service URL
    url_token_data: dict = __access_tokens.get(service_url)
    if not url_token_data:
        url_token_data = {
            "access_token": None,
            "expires_in": datetime(year=2000,
                                   month=1,
                                   day=1,
                                   tzinfo=TIMEZONE_LOCAL)
        }
        __access_tokens[service_url] = url_token_data

    # return the currently stored access token timestamp
    return url_token_data.get("expires_in")
