from abc import ABC, abstractmethod
import base64
import datetime
import hashlib
import json
import logging
import os
import uuid

import requests
from aiohttp import ClientSession

EMARSYS_URI = 'https://api.emarsys.net/'

logger = logging.getLogger(__name__)


class ApiCallError(Exception):
    pass


class BaseConnection(ABC):
    """
    Any connection used to instantiate an Emarsys object or an object inherited
     from BaseEndpoint should inherit from this class.
    this class.
    """
    @abstractmethod
    def __init__(self, username, secret, uri):
        self.username = username
        self.secret = secret
        self.uri = uri

    def build_authentication_variables(self):
        """
        Build the authentication variables Emarsys' authentication system
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

    def build_headers(self, other_headers=None):
        """
        Build the headers Emarsys' authentication system asks for.
        :return: headers.
        """
        if not other_headers:
            other_headers = {}
        nonce, created, password_digest = \
            self.build_authentication_variables()

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
            **other_headers,
        }
        return headers


class SyncConnection(BaseConnection):
    """
    Synchronous connection for Ermasys or inherited-from BaseEndpoint objects.
    """
    def __init__(self, username, secret, uri=EMARSYS_URI):
        super().__init__(username, secret, uri)

    def make_call(self,
                  method,
                  endpoint,
                  headers=None,
                  payload=None):
        """
        Make an authenticated synchronous HTTP call to the Emarsys api using
        the requests library.
        :param endpoint: Emarsys' api endpoint.
        :param method: HTTP method.
        :param headers: HTTP headers.
        :param payload: HTTP payload.
        :param params: HTTP params.
        :return: Dictionary with the result of the query.
        """
        if not payload:
            payload = {}

        url = os.path.join(self.uri, endpoint)
        headers = self.build_headers(headers)
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
                response.json()
            )


class AsyncConnection(BaseConnection):
    """
    Asynchronous connection for Ermasys or inherited-from BaseEndpoint objects.
    """
    def __init__(self, username, secret, uri=EMARSYS_URI):
        super().__init__(username, secret, uri)

    async def make_call(self,
                        method,
                        endpoint,
                        headers=None,
                        payload=None):
        """
        Make an authenticated asynchronous HTTP call to the Emarsys api using
        the aiohttp library.
        :param endpoint: Emarsys' api endpoint.
        :param method: HTTP method.
        :param headers: HTTP headers.
        :param payload: HTTP payload.
        :param params: HTTP params.
        :return: Coroutine with the result of the query.
        """
        if not payload:
            payload = {}

        url = os.path.join(self.uri, endpoint)
        headers = self.build_headers(headers)
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
