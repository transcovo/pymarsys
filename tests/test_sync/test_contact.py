import pytest
import responses

from pymarsys.sync.contact import Contact
from pymarsys import SyncEmarsys

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


class TestContact:
    @responses.activate
    def test_init_no_exception(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = SyncEmarsys(TEST_USERNAME, TEST_SECRET)
        Contact(client)

    @responses.activate
    def test_init_exception(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        with pytest.raises(TypeError):
            Contact(123)


