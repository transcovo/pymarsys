import datetime

import responses

from pymarsys.sync.sync_emarsys import SyncEmarsys

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


class TestSyncEmarsys:
    @responses.activate
    def test_sync_emarsys_init(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = SyncEmarsys(TEST_USERNAME, TEST_SECRET)

        assert client.username == TEST_USERNAME
        assert client.secret == TEST_SECRET
        assert client.uri == EMARSYS_URI
        assert client.settings == EMARSYS_SETTINGS_RESPONSE

    @responses.activate
    def test_get_authentication_variables(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = SyncEmarsys(TEST_USERNAME, TEST_SECRET)
        nonce, created, password_digest = \
            client._SyncEmarsys__get_authentication_variables()
        assert len(nonce) == 32
        assert int(nonce, 16)
        date_exceptions = 0
        for date_format in ('%Y-%m-%dT%H:%M:%S+00:00',
                            '%Y-%m-%dT%H:%M:%S',
                            '%Y-%m-%dT%H:%M:%S+0000'):
            try:
                datetime.datetime.strptime(created, date_format)
            except ValueError:
                date_exceptions += 1
        assert date_exceptions == 2
        assert len(created) == 25
        assert len(password_digest) == 56

    @responses.activate
    def test_make_call(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = SyncEmarsys(TEST_USERNAME, TEST_SECRET)
        response = client.make_call('api/v2/settings')
        assert response == EMARSYS_SETTINGS_RESPONSE






