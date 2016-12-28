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


class SyncEmarsys:
    """
    Make authenticated calls to Emarsys' API through its methods
    Usage example:
        >>> client = Emarsys(<user>, <password>)
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
    def __init__(self, username, secret, uri=EMARSYS_URI):
        self.username = username
        self.secret = secret
        self.uri = uri
        self.settings = self.make_call('api/v2/settings')
        self.contacts = Contact(self)

    def __get_authentication_variables(self):
        """
        Generate the authentication variables Emarsys' authentication system
        asks for.
        :return: nonce, created, password_digest.
        """
        nonce = uuid.uuid4().hex
        created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        sha1 = hashlib.sha1(
            str.encode(nonce + created + self.secret)
        ).hexdigest()
        password_digest = bytes.decode(base64.b64encode(str.encode(sha1)))
        return nonce, created, password_digest

    async def make_async_call(
            self,
            endpoint,
            method='GET',
            headers=None,
            payload=None,
            params=None
    ):
        """
        Make an authenticated HTTP call to the Emarsys api
        :param endpoint: Emarsys' api endpoint.
        :param method: HTTP method.
        :param headers: HTTP headers.
        :param payload: HTTP payload.
        :param params: HTTP params.
        :return: Dictionary with the result of the query.
        """

        if not headers:
            headers = {}
        if not payload:
            payload = {}
        if not params:
            params = {}

        if method not in VALID_HTTP_METHODS:
            raise ValueError(
                "'{}' is an invalid method. Valid methods are {}.".format(
                    method,
                    VALID_HTTP_METHODS,
                )
            )
        url = os.path.join(self.uri, endpoint)
        nonce, created, password_digest = self.__get_authentication_variables()

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
                    print(response)
                    return response
                else:
                    raise ApiCallError(
                        {
                            'emarsys_response': response,
                        }
                    )

    def make_call(
            self,
            endpoint,
            method='GET',
            headers=None,
            payload=None,
            params=None
    ):
        """
        Make an authenticated HTTP call to the Emarsys api
        :param endpoint: Emarsys' api endpoint.
        :param method: HTTP method.
        :param headers: HTTP headers.
        :param payload: HTTP payload.
        :param params: HTTP params.
        :return: Dictionary with the result of the query.
        """
        if not headers:
            headers = {}
        if not payload:
            payload = {}
        if not params:
            params = {}

        if method not in VALID_HTTP_METHODS:
            raise ValueError(
                "'{}' is an invalid method. Valid methods are {}.".format(
                    method,
                    VALID_HTTP_METHODS,
                )
            )
        url = os.path.join(self.uri, endpoint)
        nonce, created, password_digest = self.__get_authentication_variables()

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
            **headers,
        }
        response = requests.request(
            method,
            url,
            headers=headers,
            json=payload,
            params=params
        )
        if response.ok:
            logger.info(response.json())
            return response.json()
        else:
            raise ApiCallError(
                {
                    'emarsys_response': response.json(),
                    'original_request': response.request.__dict__
                }
            )

    def get_all_contacts(
            self,
            field_id,
            limit=None,
            offset=None,
            excludeempty=None
    ):
        """
        Gets all contacts using a field_id as index.
        :param field_id: Field ID used to generate the list.
        :param limit: Specifies the maximum number of contacts to return.
        Default is 10.000, which is also the maximum number of contacts that
        can be returned (you cannot specify more).
        :param offset: Specifies an offset for pagination (like in SQL).
        :param excludeempty: If set to true, then all contacts with a null or
        empty value in the requested field are not returned. Any value except
        for true will be interpreted as false.
        :return: Dictionary with field_id as keys, contact fields dict as
        values.
        """
        url = 'api/v2/contact/query/?return={}'.format(field_id)
        payload = {
            'limit': limit,
            'offset': offset,
            'excludeempty': excludeempty,
        }
        return self.make_async_call(url, payload=json.dumps(payload),
                                    method='GET')

    def create_contact(self, contact, key_id=None, source_id=None):
        """
        Creates a contact from a dict.
        :param contact: Key-value pairs which uniquely identify the contact
        fields which will be created for the contact (e.g. a key can be the
        email field ID (3), and its value is the email address of the specific
        contact).
        :param key_id: Key which identifies the contacts.
        :param source_id: ID assigned to the customer’s application, used to
        differentiate contacts created or modified by the external applications.
        :return: Dictionary with the id of the created contact.
        """
        payload = contact
        if key_id:
            payload['key_id'] = key_id
        if source_id:
            payload['source_id'] = source_id

        return self.make_call(
            'api/v2/contact',
            method='POST',
            payload=payload
        )

    async def async_create_multiple_contacts(
            self,
            key_id,
            contacts,
            field_id=None,
            source_id=None
    ):
        """
        Create multiple contacts
        :param key_id: Key which identifies the contacts
        :param contacts: List of key-value pairs which uniquely identify the
        contact fields which will be created for the contacts (e.g. a key can be
        the email field ID (3), and its value is the email address of the
        specific contact).
        :param field_id:
        :param source_id:
        :return: List of dictionaries with the ids of the created contacts.
        """
        payload = {
            'key_id': key_id,
            'contacts': contacts,
        }
        if field_id:
            payload['field_id'] = field_id
        if source_id:
            payload['source_id'] = source_id

        return await self.make_async_call(
            'api/v2/contact',
            method='POST',
            payload=payload
        )

    def sync_create_multiple_contacts(
            self,
            key_id,
            contacts,
            field_id=None,
            source_id=None
    ):
        """
        Create multiple contacts
        :param key_id: Key which identifies the contacts
        :param contacts: List of key-value pairs which uniquely identify the
        contact fields which will be created for the contacts (e.g. a key can be
        the email field ID (3), and its value is the email address of the
        specific contact).
        :param field_id:
        :param source_id:
        :return: List of dictionaries with the ids of the created contacts.
        """
        payload = {
            'key_id': key_id,
            'contacts': contacts,
        }
        if field_id:
            payload['field_id'] = field_id
        if source_id:
            payload['source_id'] = source_id

        return self.make_call(
            'api/v2/contact',
            method='POST',
            payload=payload
        )

    async def update_multiple_contacts(
            self,
            key_id,
            contacts,
            field_id=None,
            source_id=None,
            create_if_not_exists=False
    ):
        """
        Update multiple contacts all at once, or creates them if they do not
        exist in the database.
        :param key_id: Key which identifies the contacts.
        :param contacts: List of key-value pairs which uniquely identify the
        contact fields which will be updated for the contact (e.g. a key can be
        the email field ID (3), and its value is the email address of the
        :param field_id: ID of the field
        :param source_id: ID assigned to a customer’s external application,
        and is used to identify contacts created or modified by the external
        (3rd party) applications
        :param create_if_not_exists: Part of the URI. When enabled, if the
        contact does not exist in the database, it is created automatically.
        :return: List of dictionaries with the ids of the updated contacts.
        """
        url = 'api/v2/contact'
        if create_if_not_exists:
            url = os.path.join(url, '?create_if_not_exists=1')

        payload = {
            'key_id': key_id,
            'contacts': contacts,
        }
        if field_id:
            payload['field_id'] = field_id
        if source_id:
            payload['source_id'] = source_id
        if create_if_not_exists:
            payload['create_if_not_exists'] = create_if_not_exists

        await self.make_async_call(
            url,
            method='PUT',
            payload=payload
        )

    def delete_contact(self, contact, key_id):
        """
        Creates a contact from a contact_identifier_dict
        :param contact: Key-value pairs which uniquely identify the contact,
        e.g. a key can be the email field ID (3), and its value is the email
        address of the specific contact.
        :param key_id: Key which identifies the contact.
        :return: Empty dictionary.
        """
        payload = contact
        if key_id:
            payload['key_id'] = key_id

        return self.make_call(
            'api/v2/contact/delete',
            method='POST',
            payload=payload
        )

    def get_all_contact_lists(self):
        """
        Generate a list of the available contact lists.
        :return: List of dictionaries containing contact lists.
        """

        return self.make_call('api/v2/contactlist', method='GET')

    def get_contacts_data(self, key_id, key_values, fields=None):
        """
        :param key_id:
        :param key_values:
        :param fields:
        :return:
        """
        payload = {'keyId': key_id, 'keyValues': key_values, 'fields': fields}
        return self.make_call(
            'api/v2/contact/getdata',
            method='POST',
            payload=payload
        )

    def create_contact_list(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = 'https://api.emarsys.net/api/v2/contactlist'
        self.make_call(
            'api/v2/contactlist',
            method='POST',
            payload=kwargs
        )

    def delete_contact_list(self, list_id):
        """
        :param list_id:
        :return:
        """
        url = 'api/v2/contactlist/{}/deletelist'.format(list_id)
        return self.make_call(
            url,
            method='POST'
        )

    def delete_contacts_from_contact_list(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = 'api/v2/contactlist/{}/delete'.format(kwargs['list_id'])
        return self.make_call(
            url,
            method='POST',
            payload=kwargs
        )

    def get_all_available_fields(self):
        """
        :return:
        """
        return self.make_call('api/v2/field', method='GET')

    def create_field(self, name, application_type, string_id=None):
        """
        :param name:
        :param application_type:
        :param string_id:
        :return:
        """
        payload = {'name': name, 'application_type': application_type,
                   'string_id': string_id}
        if string_id:
            payload['string_id'] = string_id
        return self.make_call(
            'api/v2/field',
            method='POST',
            payload=payload
        )

    def delete_field(self, field_identifier_dict):
        """
        :param field_identifier_dict:
        :return:
        """
        return self.make_call(
            'api/v2/field/delete',
            method='POST',
            payload=field_identifier_dict
        )
