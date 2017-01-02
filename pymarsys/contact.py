from .base_endpoint import BaseEndpoint


class Contact(BaseEndpoint):
    """
    Class representation of the Contacts endpoint.
    """
    def __init__(self, connection, endpoint='api/v2/contact'):
        super().__init__(connection, endpoint)

    def create(self, contact, key_id=None, source_id=None):
        """
        Create a contact from a dict.
        :param contact: Key-value pairs which uniquely identify the contact
        fields which will be created for the contact (e.g. a key can be the
        email field ID (3), and its value is the email address of the specific
        contact).
        :param key_id: Key which identifies the contacts.
        :param source_id: ID assigned to the customer’s application, used to
        differentiate contacts created or modified by the external
        applications.
        :return: Dictionary with the id of the created contact.
        """
        payload = contact
        if key_id:
            payload['key_id'] = key_id
        if source_id:
            payload['source_id'] = source_id

        return self.connection.make_call(
            'POST',
            self.endpoint,
            payload=payload
        )
