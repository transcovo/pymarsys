from .contact import Contact


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
