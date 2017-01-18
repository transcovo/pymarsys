from .contact import Contact
from .contact_field import ContactField


class Emarsys:
    """
    Make authenticated calls to Emarsys' API through its attributes.
    Usage example:
        >>> connection = SyncConnection(<user>, <password>)
        >>> client = Emarsys(connection)
        >>> client.contacts.create({'3': 'squirrel@squirrelmail.com'})
        {'data': {'id': 123456789}, 'replyCode': 0, 'replyText': 'OK'}

    """
    def __init__(self, connection):
        self.connection = connection
        self.contacts = Contact(self.connection)
        self.contact_fields = ContactField(self.connection)
