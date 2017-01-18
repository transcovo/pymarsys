from .base_endpoint import BaseEndpoint


class ContactField(BaseEndpoint):
    """
    Class representation of the Contact Fields endpoint.

    Examples:
    If you want to use contact_fields' methods through an instance of the
    Emarsys client:
    >>> from pymarsys import SyncConnection, Emarsys
    >>> connection = SyncConnection('username', 'password')
    >>> client = Emarsys(connection)
    >>> client.contact_fields
    <pymarsys.contact_field.ContactField at 0x10cd8d9e8>

    If you want to use contact_fields' methods through an instance of the
    ContactField endpoint class:
    >>> from pymarsys import SyncConnection
    >>> from pymarsys.contact_field import ContactField
    >>> connection = SyncConnection('username', 'password')
    >>> contact_fields = ContactField(connection)
    >>> contact_fields
    <pymarsys.contact_field.ContactField at 0x10cd8db70>
    """
    def __init__(self, connection, endpoint='api/v2/field/'):
        super().__init__(connection, endpoint)

    def create(self, name, application_type, string_id=None):
        """
        Creates a new field in your contact database. This matches the
        functionality of the Field Generator in the application (Admin menu
        > Field Editor > New). Please note that you cannot create single- or
        multi-choice fields via the API, nor can you create more than one
        field at a time.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/create-field/

        :param name: Name of the new field.
        :param application_type: Type of the new field. Supported types:
        shorttext (max 60 characters), longtext (max 255 characters),
        largetext (theoretically unlimited characters), date, url, numeric
        (max 24 digits).
        :param string_id: ID of the new field.
        :return: Internal id of the created field.

        Examples:
        If you want to create a new shorttext field called squirrel_field:
        >>> client.contact_fields.create('squirrel_field', 'shorttext')
        {
            'data': {
                'application_type': 'shorttext',
                'id': 3106,
                'name': 'squirrel_field',
                'string_id': 'squirrel_field'
            },
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        payload = {
            'name': name,
            'application_type': application_type
        }

        if string_id:
            payload['string_id'] = string_id

        return self.connection.make_call(
            'POST',
            self.endpoint,
            payload=payload
        )

    def list(self, translate_id=None):
        """
        Returns a list of all available fields which can be used to
        personalize content (including custom fields and vouchers).
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/list-fields/

        :param translate: Any two letter ISO 639-1 abbreviation, e.g. en, de,
        ru, etc.
        :return: List of contact fields, translated or not.

        Examples:
        If you want to get your list of available fields translated to Spanish:
        >>> client.contact_fields.list('es')
        {
            'data': [
                {
                    'application_type': 'interests',
                    'id': 0,
                    'name': 'Intereses',
                    'string_id': 'interests'
                },
                {
                    'application_type': 'singlechoice',
                    'id': 9,
                    'name': 'Título académico',
                    'string_id': 'title'
                }
                ...
            ],
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        if translate_id:
            query_endpoint = '{}/{}/{}'.format(
                self.endpoint,
                'translate',
                translate_id
            )
        else:
            query_endpoint = str(self.endpoint)

        return self.connection.make_call(
            'GET',
            query_endpoint
        )

    def list_choice(self, list_id, translate_id=None):
        """
        Generates a list of all available options for any given single- or
        multi-choice field.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/list-field-choices/

        :param list_id: Field ID.
        :param translate_id: Lists available translations where lang defines
        the target language (e.g. fr, ru, etc.)
        :return: List of all available options for any given single- or
        multi-choice field.

        Examples:
        If you want to get the available options for the Opt-in field:
        >>> client.contact_fields.list_choice(31)
        {
            'data': [
                {'choice': 'True', 'id': '1'},
                {'choice': 'False', 'id': '2'}
            ],
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        query_endpoint = '{}/{}/{}'.format(self.endpoint, list_id, 'choice')
        if translate_id:
            query_endpoint = '{}/{}/{}'.format(
                query_endpoint,
                'translate',
                translate_id
            )

        return self.connection.make_call(
            'GET',
            query_endpoint
        )

    def last_change(self, key_id, key_value, field_id):
        """
        Returns the date and time, the old value and the current value of the
        latest change of a given contact field.
        http://documentation.emarsys.com/resource/querying-a-contact-field-change/

        :param key_id: Key which identifies the contacts. This can be a field
        ID, ID, UID or EID.
        :param key_value: Key field value to use in the query.
        :param field_id: This can be a field ID only.
        :return: List with old and current values.

        Examples:
        If you want to get the last changes on the Opt-in field for the contact
        which email is squirrel@squirrelmail.com:
        >>> client.contact_fields.last_change(
        ...     3,
        ...     'squirrel@squirrelmail.com',
        ...     31
        ... )
        {
            'data': {
                'current_value': '1',
                'old_value': '2',
                'time': '2017-01-17 14:46:28'
            },
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        query_endpoint = 'api/v2/contact/last_change/'
        params = {
            'key_id': key_id,
            'key_value': key_value,
            'field_id': field_id,
        }

        return self.connection.make_call(
            'GET',
            query_endpoint,
            params=params
        )
