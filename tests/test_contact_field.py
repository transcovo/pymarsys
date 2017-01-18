import pytest
import responses
from urllib.parse import urljoin

from pymarsys.connections import SyncConnection
from pymarsys.contact_field import ContactField

EMARSYS_URI = 'https://api.emarsys.net/'
CONTACT_ENDPOINT = 'api/v2/contact/'
CONTACT_FIELDS_ENDPOINT = 'api/v2/field/'
TEST_USERNAME = 'test_username'
TEST_SECRET = 'test_secret'
TEST_SETTINGS = {'test': 'settings'}

EMARSYS_CONTACT_FIELDS_CREATE_RESPONSE = {
    'data': {
        'application_type': 'longtext',
        'id': 2670,
        'name': 'test field4',
        'string_id': 'test_field4'
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACT_FIELDS_LIST_RESPONSE = {
    'data': [
        {
            'application_type': 'longtext',
            'id': 0,
            'name': 'Squirrel Field',
            'string_id': 'squirrel_field'
        },
    ],
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACT_FIELDS_LIST_CHOICE_RESPONSE = {
    'data': [{'choice': 'Male', 'id': '1'}, {'choice': 'Female', 'id': '2'}],
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACT_FIELDS_LAST_CHANGE = {
    'data': {
        'current_value': 'Squirrel The First',
        'old_value': 'Squirrel',
        'time': '2017-01-06 21:04:55'
    },
    'replyCode': 0,
    'replyText': 'OK'
}


class TestContactField:
    def test_init_no_exception(self):
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        ContactField(connection)

    def test_init_exception(self):
        with pytest.raises(TypeError):
            ContactField(123)

    @responses.activate
    def test_create(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, CONTACT_FIELDS_ENDPOINT),
            json=EMARSYS_CONTACT_FIELDS_CREATE_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contact_fields = ContactField(connection)

        response = contact_fields.create('squirrel_field', 'longtext')
        assert response == EMARSYS_CONTACT_FIELDS_CREATE_RESPONSE

    @responses.activate
    def test_list(self):
        responses.add(
            responses.GET,
            urljoin(EMARSYS_URI, CONTACT_FIELDS_ENDPOINT),
            json=EMARSYS_CONTACT_FIELDS_LIST_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contact_fields = ContactField(connection)

        response = contact_fields.list()
        assert response == EMARSYS_CONTACT_FIELDS_LIST_RESPONSE

    @responses.activate
    def test_list_choice(self):
        responses.add(
            responses.GET,
            urljoin(
                EMARSYS_URI, '{}/{}/{}'.format(
                    CONTACT_FIELDS_ENDPOINT,
                    5,
                    'choice'
                )
            ),
            json=EMARSYS_CONTACT_FIELDS_LIST_CHOICE_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contact_fields = ContactField(connection)

        response = contact_fields.list_choice(5)
        assert response == EMARSYS_CONTACT_FIELDS_LIST_CHOICE_RESPONSE

    @responses.activate
    def test_last_change(self):
        responses.add(
            responses.GET,
            urljoin(
                EMARSYS_URI,
                '{}/{}'.format(
                    CONTACT_ENDPOINT,
                    'last_change/?key_id=3&key_value=squirrel@squirrelmail.com'
                    '&field_id=1'
                )
            ),
            json=EMARSYS_CONTACT_FIELDS_LAST_CHANGE,
            status=200,
            content_type='application/json',
            match_querystring=True
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contact_fields = ContactField(connection)

        response = contact_fields.last_change(
            3,
            'squirrel@squirrelmail.com',
            1
        )
        assert response == EMARSYS_CONTACT_FIELDS_LAST_CHANGE
