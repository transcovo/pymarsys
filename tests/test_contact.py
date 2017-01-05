import pytest
import responses
from urllib.parse import urljoin

from pymarsys.connections import SyncConnection
from pymarsys.contact import Contact

EMARSYS_URI = 'https://api.emarsys.net/'
CONTACT_ENDPOINT = 'api/v2/contact/'
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

EMARSYS_CONTACTS_CREATE_RESPONSE = {
    'data': {'id': 123456789},
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_CREATE_MANY_RESPONSE = {
    'data': {
        'ids': [523033975, 523033197]
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_LIST_DATA_RESPONSE = {
    'data': {
        'errors': [],
        'result': [
            {'3': 'squirrel1@squirrelmail.com', 'id': '748488446'},
            {'3': 'squirrel2@squirrelmail.com', 'id': '752737075'},
        ]
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_GET_DATA_RESPONSE = {
    'data': {
        'errors': [],
        'result': [
            {
                '1': 'Squirrel1',
                '2': 'Squirrou1',
                '3': 'squirrel1@squirrelmail.com',
                'id': '748473102',
                'uid': 'hVXGDiKg6d'
            },
            {
                '1': 'Squirrel2',
                '2': 'Squirrou2',
                '3': 'squirrel2@squirrelmail.com',
                'id': '752469438',
                'uid': 'g8XS7T1weS'
            }
        ]
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_GET_CONTACT_HISTORY_RESPONSE = {
    'data': [
        {
            'bounce_status': '',
            'contactId': '723005829',
            'delivery_status': 'launched',
            'emailId': 3109,
            'launchListId': '77',
            'launch_date': '2016-12-23 07:00:00'
        }
    ],
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_FETCH_INTERNAL_ID_RESPONSE = {
    'data': {
        'id': '752469438'
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_CHECK_IDS_RESPONSE = {
    'data': {
        'errors': [],
        'ids': {
            'Squirrel1': ['748488446', '772789701'],
            'Squirrel2': ['754121205', '748473102']
        }
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_UPDATE_RESPONSE = {
    'data': {'id': '653298763'},
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_UPDATE_MANY_RESPONSE = {
    'data': {
        'ids': ['653298763', '657196356']
    },
    'replyCode': 0,
    'replyText': 'OK'
}

EMARSYS_CONTACTS_DELETE_RESPONSE = {
    'data': {
        'id': 658060758
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
            urljoin(EMARSYS_URI, CONTACT_ENDPOINT),
            json=EMARSYS_CONTACTS_CREATE_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.create({'3': 'squirrel@squirrelmail.com'})
        assert response == EMARSYS_CONTACTS_CREATE_RESPONSE

    @responses.activate
    def test_create_many(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, CONTACT_ENDPOINT),
            json=EMARSYS_CONTACTS_CREATE_MANY_RESPONSE,
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
        assert response == EMARSYS_CONTACTS_CREATE_MANY_RESPONSE

    @responses.activate
    def test_list_data(self):
        responses.add(
            responses.GET,
            urljoin(
                EMARSYS_URI,
                '{}/{}'.format(
                    CONTACT_ENDPOINT, 'query/?return=3&limit=2&1=Squirrel'
                )
            ),
            json=EMARSYS_CONTACTS_LIST_DATA_RESPONSE,
            status=200,
            content_type='application/json',
            match_querystring=True
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.query(
            3,
            field_id_dict={1: 'Squirrel'},
            limit=2
        )
        assert response == EMARSYS_CONTACTS_LIST_DATA_RESPONSE

    @responses.activate
    def test_get_data(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, '{}/{}/'.format(CONTACT_ENDPOINT, 'getdata')),
            json=EMARSYS_CONTACTS_GET_DATA_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.get_data(
            '3',
            ['squirrel1@squirrelmail.com', 'squirrel2@squirrelmail.com'],
            [1, 2, 3]
        )
        assert response == EMARSYS_CONTACTS_GET_DATA_RESPONSE

    @responses.activate
    def test_get_history(self):
        responses.add(
            responses.POST,
            urljoin(
                EMARSYS_URI,
                '{}/{}/'.format(CONTACT_ENDPOINT, 'getcontacthistory')
            ),
            json=EMARSYS_CONTACTS_GET_CONTACT_HISTORY_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.get_history(
            [723005829]
        )
        assert response == EMARSYS_CONTACTS_GET_CONTACT_HISTORY_RESPONSE

    @responses.activate
    def test_fetch_internal_id(self):
        responses.add(
            responses.GET,
            urljoin(
                EMARSYS_URI,
                '{}/{}'.format(
                    CONTACT_ENDPOINT,
                    '?3=squirrel@squirrelmail.com'
                )
            ),
            json=EMARSYS_CONTACTS_FETCH_INTERNAL_ID_RESPONSE,
            status=200,
            content_type='application/json',
            match_querystring=True
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.fetch_internal_id(
            3,
            'squirrel@squirrelmail.com'
        )
        assert response == EMARSYS_CONTACTS_FETCH_INTERNAL_ID_RESPONSE

    @responses.activate
    def test_check_ids(self):
        responses.add(
            responses.POST,
            urljoin(
                EMARSYS_URI,
                '{}/{}/'.format(CONTACT_ENDPOINT, 'checkids')
            ),
            json=EMARSYS_CONTACTS_CHECK_IDS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.check_ids('1', ['Squirrel1', 'Squirrel2'], True)
        assert response == EMARSYS_CONTACTS_CHECK_IDS_RESPONSE

    @responses.activate
    def test_update(self):
        responses.add(
            responses.PUT,
            urljoin(EMARSYS_URI, CONTACT_ENDPOINT),
            json=EMARSYS_CONTACTS_CHECK_IDS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.update(
            {'3': 'squirrel_new@squirrel.com', '1': 'Squirrel'},
            key_id=1
        )
        assert response == EMARSYS_CONTACTS_CHECK_IDS_RESPONSE

    @responses.activate
    def test_update_many(self):
        responses.add(
            responses.PUT,
            urljoin(EMARSYS_URI, CONTACT_ENDPOINT),
            json=EMARSYS_CONTACTS_UPDATE_MANY_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.update_many(
            '3',
            [
                {'3': 'squirrel1@squirrel.com', '1': 'Squirrel 1 New Name'},
                {'3': 'squirrel2@squirrel.com', '1': 'Squirrel 2 New Name'},
            ]
        )
        assert response == EMARSYS_CONTACTS_UPDATE_MANY_RESPONSE

    @responses.activate
    def test_delete(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, '{}/{}/'.format(CONTACT_ENDPOINT, 'delete')),
            json=EMARSYS_CONTACTS_DELETE_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contacts = Contact(connection)

        response = contacts.delete(
            {'3': 'squirrel@squirrel.com'},
        )
        assert response == EMARSYS_CONTACTS_DELETE_RESPONSE
