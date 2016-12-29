import asyncio
import base64
import datetime
import hashlib
import json
import logging
import os
import uuid

from aiohttp import ClientSession
import requests

from .contact import Contact

VALID_HTTP_METHODS = ('GET', 'POST', 'PUT', 'DELETE')
EMARSYS_URI = 'https://api.emarsys.net/'

logger = logging.getLogger(__name__)


class ApiCallError(Exception):
    pass


class Emarsys:
    """
    Make authenticated calls to Emarsys' API through its methods
    Usage example:
        >>> client = Emarsys('sync', <user>, <password>)
        >>> client.settings
        >>> {
                'data': {
                    'country': 'France',
                    'environment': 'suite16.emarsys.net',
                    'id': 123456789,
                    'name': 'name',
                    'password_history_queue_size': 1,
                    'timezone': 'Europe/Vienna',
                    'totalContacts': '1'
                },
                'replyCode': 0,
                'replyText': 'OK'
            }
    """
    def __init__(self, username, secret, uri=EMARSYS_URI, is_async=False):
        emarsys_settings_endpoint = 'api/v2/settings'
        self.is_async = is_async
        self.username = username
        self.secret = secret
        self.uri = uri
        if self.is_async:
            self.make_call = self.__make_async_call
            loop = asyncio.get_event_loop()
            self.settings = loop.run_until_complete(
                self.make_call(emarsys_settings_endpoint)
            )
        else:
            self.make_call = self.__make_sync_call
            self.settings = self.make_call(emarsys_settings_endpoint)
        self.contacts = Contact(self)

    def __build_authentication_variables(self):
        """
        Generate the authentication variables Emarsys' authentication system
        asks for.
        :return: nonce, created, password_digest.
        """
        nonce = uuid.uuid4().hex
        created = datetime.datetime.utcnow().strftime(
            '%Y-%m-%dT%H:%M:%S+00:00'
        )
        sha1 = hashlib.sha1(
            str.encode(nonce + created + self.secret)
        ).hexdigest()
        password_digest = bytes.decode(base64.b64encode(str.encode(sha1)))
        return nonce, created, password_digest

    def __build_headers(self, headers):
        if not headers:
            headers = {}
        nonce, created, password_digest = \
            self.__build_authentication_variables()

        http_header = ','.join(
            (
                'UsernameToken Username="{}"'.format(self.username),
                'PasswordDigest="{}"'.format(password_digest),
                'Nonce="{}"'.format(nonce),
                'Created="{}"'.format(created),
            )
        )
        headers = {
            'X-WSSE': http_header,
            'Content-Type': 'application/json',
            **headers,
        }
        return headers

    def __make_sync_call(self,
                         endpoint,
                         method='GET',
                         headers=None,
                         payload=None):
        """
        Make an authenticated HTTP call to the Emarsys api
        :param endpoint: Emarsys' api endpoint.
        :param method: HTTP method.
        :param headers: HTTP headers.
        :param payload: HTTP payload.
        :param params: HTTP params.
        :return: Dictionary with the result of the query.
        """
        if method not in VALID_HTTP_METHODS:
            raise ValueError(
                "'{}' is an invalid method. Valid methods are {}.".format(
                    method,
                    VALID_HTTP_METHODS,
                )
            )
        if not payload:
            payload = {}

        url = os.path.join(self.uri, endpoint)
        headers = self.__build_headers(headers)
        response = requests.request(
            method,
            url,
            headers=headers,
            json=payload
        )
        if response.ok:
            logger.info(response.json())
            return response.json()
        else:
            raise ApiCallError(
                {
                    'emarsys_response': response.json(),
                }
            )

    async def __make_async_call(self,
                                endpoint,
                                method='GET',
                                headers=None,
                                payload=None):
        """
        Make an authenticated HTTP call to the Emarsys api
        :param endpoint: Emarsys' api endpoint.
        :param method: HTTP method.
        :param headers: HTTP headers.
        :param payload: HTTP payload.
        :param params: HTTP params.
        :return: Dictionary with the result of the query.
        """
        if method not in VALID_HTTP_METHODS:
            raise ValueError(
                "'{}' is an invalid method. Valid methods are {}.".format(
                    method,
                    VALID_HTTP_METHODS,
                )
            )
        if method not in VALID_HTTP_METHODS:
            raise ValueError(
                "'{}' is an invalid method. Valid methods are {}.".format(
                    method,
                    VALID_HTTP_METHODS,
                )
            )
        if not payload:
            payload = {}

        url = os.path.join(self.uri, endpoint)
        headers = self.__build_headers(headers)
        async with ClientSession() as session:
            async with session.request(
                    method,
                    url,
                    headers=headers,
                    data=json.dumps(payload)
            ) as response:
                response = await response.json()
                if response['replyCode'] == 0:
                    logger.info(response)
                    return response
                else:
                    raise ApiCallError(
                        response
                    )
