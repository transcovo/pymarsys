from .base_endpoint import BaseEndpoint


class ContactList(BaseEndpoint):
    """
    Class representation of the ContactList endpoint.

    Examples:
    If you want to use contact lists' methods through an instance of the Emarsys
    client:
    >>> from pymarsys import SyncConnection, Emarsys
    >>> connection = SyncConnection('username', 'password')
    >>> client = Emarsys(connection)
    >>> client.contact_list
    <pymarsys.contact_list.ContactList at 0x1050f7048>

    If you want to use contact lists' methods trough an instance of the ContactList
    endpoint class:
    >>> from pymarsys import SyncConnection
    >>> from pymarsys.contact_list import ContactList
    >>> connection = SyncConnection('username', 'password')
    >>> contact_list = ContactList(connection)
    >>> contact_list
    <pymarsys.contact_list.ContactList at 0x10333ec88>
    """

    def __init__(self, connection, endpoint="api/v2/contactlist/"):
        super().__init__(connection, endpoint)

    def create(self, name, key_id=3, with_contacts_ids=None, description=None):
        """
        Create a contact list.
        https://dev.emarsys.com/v2/contact-lists/create-a-contact-list
        :param name: name of the list to create
        :param key_id: Key which identifies the contact. This can be a field
        id, id, uid or eid. If left empty, the email address (field ID 3) will
        be used by default.
        :param with_contacts_ids: list of key's value to add to the list. e.g. ['squirrel@squirrelmail.com',]
        :param description: Additional information about the contact list.
        :return: The API response payload.
.
        Examples:
        If you want to create a list which name is test_list and assign squirrel@squirrelmail.com to this list:
        >>> client.lists.create("test_list", ['squirrel@squirrelmail.com',])
        {'data': {'id': 123}, 'replyCode': 0, 'replyText': 'OK'}
        """
        payload = {
            "key_id": key_id,
            "name": name,
            "description": description,
            "external_ids": with_contacts_ids,
        }

        return self.connection.make_call("POST", self.endpoint, payload=payload)

    def add_contacts(self, list_id, contacts_ids, key_id=3):
        """
        Add multiple contacts to an existing list.
        https://dev.emarsys.com/v2/contact-lists/add-contacts-to-a-contact-list

        :param list_id: Identifier of the list you want to add a contact to.
        :param contacts_ids: List of contact identifier you want to add to the list
        :param key_id: Key which identifies the contact. This can be a field
        id, id, uid or eid. If left empty, the email address (field ID 3) will
        be used by default.
        :return: The API response payload.

        Examples:
        If you want to add two squirrel1@squirrelmail.com to the list test_list:
        >>> client.contact_list.add('test_list', ['squirrel1@squirrelmail.com',])
        {'data': {'inserted_contacts': 123}, 'replyCode': 0, 'replyText': 'OK'}
        """

        payload = {"key_id": key_id, "external_ids": contacts_ids}

        endpoint = "{}{}/add/".format(self.endpoint, list_id)
        return self.connection.make_call("POST", endpoint, payload=payload)
