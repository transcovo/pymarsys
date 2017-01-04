import asyncio
import datetime
from urllib.parse import urljoin

from aioresponses import aioresponses
import responses

from pymarsys.connections import (
    BaseConnection,
    SyncConnection,
    AsyncConnection,
)

EMARSYS_URI = 'https://api.emarsys.net/'
TEST_USERNAME = 'test_username'
TEST_SECRET = 'test_secret'

EMARSYS_SETTINGS_RESPONSE = {
    'data': {
        'country': 'France',
        'environment': 'suite16.emarsys.net',
        'id': 123456789,
        'name': 'testname',
        'password_history_queue_size': 1,
        'timezone': 'Europe/Paris',
        'totalContacts': '111111'
    },
    'replyCode': 0,
    'replyText': 'OK'
}


class TestBaseConnection():
    def test_build_authentication_variables(self):
        BaseConnection.__abstractmethods__ = frozenset()
        connection = BaseConnection(TEST_USERNAME, TEST_SECRET, EMARSYS_URI)
        nonce, created, password_digest = \
            connection.build_authentication_variables()
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


class TestSyncConnection():
    def test_init(self):
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET, EMARSYS_URI)

        assert connection.username == TEST_USERNAME
        assert connection.secret == TEST_SECRET
        assert connection.uri == EMARSYS_URI

    @responses.activate
    def test_make_call(self):
        responses.add(
            responses.GET,
            urljoin(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET, EMARSYS_URI)

        response = connection.make_call('GET', 'api/v2/settings')
        assert response == EMARSYS_SETTINGS_RESPONSE


class TestAsyncConnection():
    def test_init(self):
        connection = AsyncConnection(
            TEST_USERNAME,
            TEST_SECRET,
            EMARSYS_URI
        )

        assert connection.username == TEST_USERNAME
        assert connection.secret == TEST_SECRET
        assert connection.uri == EMARSYS_URI

    def test_make_call(self):
        connection = AsyncConnection(
            TEST_USERNAME,
            TEST_SECRET,
            EMARSYS_URI
        )
        with aioresponses() as m:
            m.get(
                '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
                status=200,
                payload=EMARSYS_SETTINGS_RESPONSE
            )
            coroutine = connection.make_call('GET', 'api/v2/settings')
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(coroutine)
            assert response == EMARSYS_SETTINGS_RESPONSE
