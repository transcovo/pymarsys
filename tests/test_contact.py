import pytest
import responses
from urllib.parse import urljoin

from pymarsys.connections import SyncConnection
from pymarsys.contact import Contact

EMARSYS_URI = 'https://api.emarsys.net/'
TEST_USERNAME = 'test_username'
TEST_SECRET = 'test_secret'
TEST_SETTINGS = {'test': 'settings'}

EMARSYS_SETTINGS_RESPONSE = {
    'data': {
        'country': 'France',
        'environment': 'suite16.emarsys.net',
        'id': 123456789,
        'name': 'testname',
        'password_history_queue_size': 1,
        'timezone': 'Europe/Vienna',
        'totalContacts': '111111'
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CREATE_CONTACT_RESPONSE = {
    'data': {'id': 123456789},
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CREATE_MANY_CONTACTS_RESPONSE = {
    'data': {
        'ids': [523033975, 523033197]
    },
    'replyCode': 0,
    'replyText': 'OK'
}


class TestContact:
    def test_init_no_exception(self):
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        Contact(connection)

    def test_init_exception(self):
        with pytest.raises(TypeError):
            Contact(123)

    @responses.activate
    def test_create(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, 'api/v2/contact'),
            json=EMARSYS_CREATE_CONTACT_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.create({'3': 'squirrel@squirrelmail.com'})
        assert response == EMARSYS_CREATE_CONTACT_RESPONSE

    @responses.activate
    def test_create_many(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, 'api/v2/contact'),
            json=EMARSYS_CREATE_MANY_CONTACTS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.create_many(
            [
                {'3': 'squirrel1@squirrelmail.com'},
                {'3': 'squirrel2@squirrelmail.com'},
            ]
        )
        assert response == EMARSYS_CREATE_MANY_CONTACTS_RESPONSE
