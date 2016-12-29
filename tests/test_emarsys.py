import asyncio
import datetime

from aioresponses import aioresponses
import responses

from pymarsys.emarsys import Emarsys

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


class TestAnyEmarsys:
    @responses.activate
    def test_build_authentication_variables(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = Emarsys(TEST_USERNAME, TEST_SECRET)
        nonce, created, password_digest = \
            client._Emarsys__build_authentication_variables()
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


class TestSyncEmarsys:
    @responses.activate
    def test_init(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = Emarsys(TEST_USERNAME, TEST_SECRET)

        assert client.username == TEST_USERNAME
        assert client.secret == TEST_SECRET
        assert client.uri == EMARSYS_URI
        assert client.settings == EMARSYS_SETTINGS_RESPONSE

    @responses.activate
    def test_make_call(self):
        responses.add(
            responses.GET,
            '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
            json=EMARSYS_SETTINGS_RESPONSE,
            status=200,
            content_type='application/json'
        )
        client = Emarsys(TEST_USERNAME, TEST_SECRET)
        response = client.make_call('api/v2/settings')
        assert response == EMARSYS_SETTINGS_RESPONSE


class TestAsyncEmarsys:
    def test_init(self):
        with aioresponses() as m:
            m.get(
                '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
                status=200,
                payload=EMARSYS_SETTINGS_RESPONSE
            )
            client = Emarsys(TEST_USERNAME, TEST_SECRET, is_async=True)

            assert client.username == TEST_USERNAME
            assert client.secret == TEST_SECRET
            assert client.uri == EMARSYS_URI
            assert client.settings == EMARSYS_SETTINGS_RESPONSE

    def test_make_call(self):
        with aioresponses() as m:
            m.get(
                '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
                status=200,
                payload=EMARSYS_SETTINGS_RESPONSE
            )
            client = Emarsys(TEST_USERNAME, TEST_SECRET, is_async=True)
        with aioresponses() as m:
            m.get(
                '{}{}'.format(EMARSYS_URI, 'api/v2/settings'),
                status=200,
                payload=EMARSYS_SETTINGS_RESPONSE
            )
            coroutine = client.make_call('api/v2/settings')
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(coroutine)
            assert response == EMARSYS_SETTINGS_RESPONSE
