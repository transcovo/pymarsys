import pytest
import responses
from urllib.parse import urljoin

from pymarsys.connections import SyncConnection
from pymarsys.contact_list import ContactList

EMARSYS_URI = "https://api.emarsys.net/"
CONTACT_LIST_ENDPOINT = "api/v2/contactlist/"
TEST_USERNAME = "test_username"
TEST_SECRET = "test_secret"

EMARSYS_CONTACT_LIST_CREATE_RESPONSE = {
    "replyCode": 0,
    "replyText": "OK",
    "data": {"id": 1},
}

ADD_TO_CONTACT_LIST_ENDPOINT = "api/v2/contactlist/1/add/"


EMARSYS_ADD_TO_CONTACT_LIST_RESPONSE = {
    "replyCode": 0,
    "replyText": "OK",
    "data": {"inserted_contacts": 1},
}

class TestContactList:
    def test_init_no_exception(self):
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        ContactList(connection)

    def test_init_exception(self):
        with pytest.raises(TypeError):
            ContactList(123)

    @responses.activate
    def test_create(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, CONTACT_LIST_ENDPOINT),
            json=EMARSYS_CONTACT_LIST_CREATE_RESPONSE,
            status=200,
            content_type="application/json",
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contact_list = ContactList(connection)
        response = contact_list.create("test_list")
        assert response == EMARSYS_CONTACT_LIST_CREATE_RESPONSE

    @responses.activate
    def test_add_contacts(self):
        responses.add(
            responses.POST,
            urljoin(EMARSYS_URI, ADD_TO_CONTACT_LIST_ENDPOINT),
            json=EMARSYS_ADD_TO_CONTACT_LIST_RESPONSE,
            status=200,
            content_type="application/json",
        )
        connection = SyncConnection(TEST_USERNAME, TEST_SECRET)
        contact_list = ContactList(connection)

        response = contact_list.add_contacts(1, ["squirrel1@squirrelmail.com"])
        assert response == EMARSYS_ADD_TO_CONTACT_LIST_RESPONSE
