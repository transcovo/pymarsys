from .base_endpoint import BaseEndpoint


class Contact(BaseEndpoint):
    """
    Class representation of the Contacts endpoint.

    Examples:
    If you want to use contacts' methods through an instance of the Emarsys
    client:
    >>> from pymarsys import SyncConnection, Emarsys
    >>> connection = SyncConnection('username', 'password')
    >>> client = Emarsys(connection)
    >>> client.contacts
    <pymarsys.contact.Contact at 0x1050f7048>

    If you want to use contacts' methods trough an instance of the Contact
    endpoint class:
    >>> from pymarsys import SyncConnection
    >>> from pymarsys.contact import Contact
    >>> connection = SyncConnection('username', 'password')
    >>> contacts = Contact(connection)
    >>> contacts
    <pymarsys.contact.Contact at 0x10333ec88>
    """
    def __init__(self, connection, endpoint='api/v2/contact/'):
        super().__init__(connection, endpoint)

    def create(self, contact, key_id=None, source_id=None):
        """
        Create a contact from a dictionary.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/create-contact/

        :param contact: Key-value pairs which uniquely identify the contact
        fields which will be created for the contact (e.g. a key can be the
        email field ID (3), and its value is the email address of the specific
        contact).
        :param key_id: Key which identifies the contact. This can be a field
        id, id, uid or eid. If left empty, the email address (field ID 3) will
        be used by default.
        :param source_id: ID assigned to the customer’s application, used to
        differentiate contacts created or modified by the external
        applications.
        :return: Dictionary with the id of the created contact.

        Examples:
        If you want to create a contact which email is
        squirrel@squirrelmail.com, which first name is Donald and which last
        name is Trump:
        >>> client.contacts.create(
        ...     {3: 'squirrel@squirrelmail.com', 1: 'Donald', 2: 'Trump'}
        ... )
        {'data': {'id': 588585705}, 'replyCode': 0, 'replyText': 'OK'}
        """
        payload = dict(contact)
        if key_id:
            payload['key_id'] = key_id
        if source_id:
            payload['source_id'] = source_id

        return self.connection.make_call(
            'POST',
            self.endpoint,
            payload=payload
        )

    def create_many(self, contacts, key_id=None):
        """
        Create many contacts from a list of dictionaries.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/create-multiple-contacts/

        :param contacts: A list of key-value pairs which uniquely identify
        the contact fields which will be created for the contact (e.g. a key
        can be the email field ID (3), and its value is the email address of
        the specific contact).
        :param key_id: Key which identifies the contacts. This can be a field
        id, id or uid. If left empty, the internal ID will be used by default.
        :return: Dictionary with a list of the ids of the created contacts.

        Examples:
        If you want to create two contacts which emails are
        squirrel1@squirrelmail.com and squirrel1@squirrelmail.com, which first
        names are Donald and Barack and which last names are Trump and Obama:
        >>> client.contacts.create_many(
        ...     [
        ...         {3: 'squirrel1@squirrelmail.com', 1: 'Donald', 2: 'Trump'},
        ...         {3: 'squirrel2@squirrelmail.com', 1: 'Barack', 2: 'Obama'},
        ...     ]
        ... )
        {
            'data': {'ids': [589058827, 589058576]},
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        payload = {
            'contacts': contacts,
        }
        if key_id:
            payload['key_id'] = key_id

        return self.connection.make_call(
            'POST',
            self.endpoint,
            payload=payload
        )

    def query(self,
              field_id_to_return,
              query_tuple=None,
              limit=None,
              offset=None,
              exclude_empty=None):
        """
        Generate a list of contacts with values for a specific field. For
        example, field_id 1 returns the first names of all contacts. Both the
        values and the contact IDs are returned.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/list-contact-data/

        :param field_id_to_return: Field ID used to generate the list.
        :param query_tuple: The first item on the tuple is the field_id,
        the second item is the value of the field, it determines if a contact
        should be returned or not. The value can be an empty string as that
        will also match to cells with NULL value.
        :param limit: Specifies the maximum number of contacts to return.
        Default is 10.000, which is also the maximum number of contacts that
        can be returned (you cannot specify more).
        :param offset: Specifies an offset for pagination (like in SQL).
        :param exclude_empty: If set to true, then all contacts with a null
        or empty value in the requested field are not returned. Any value
        except for true will be interpreted as false.
        :return: List of contacts.

        Examples:
        If you want to get all the first names of all the contacts which last
        name is Trump:
        >>> client.contacts.query(1, (2, 'Trump'))
        {
            'data': {
                'errors': [],
                 'result': [{'1': 'Donald', 'id': '589058827'}]
            },
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'query')
        params = {
            'return': field_id_to_return,
        }

        if limit is not None:
            params['limit'] = limit

        if limit is not None:
            params['offset'] = offset

        if limit is not None:
            params['excludeempty'] = exclude_empty

        if query_tuple is not None:
            if len(query_tuple) > 2:
                raise ValueError(
                    'query_tuple should contain only one field_id and '
                    'one value'
                )
            params[query_tuple[0]] = query_tuple[1]

        return self.connection.make_call(
            'GET',
            query_endpoint,
            params=params
        )

    def get_data(self,
                 key_id,
                 key_values,
                 fields=None):
        """
        Returns the values of specified fields for contacts. The contacts can
        be specified by using either the internal IDs or by using another
        column value.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/contact-data/

        :param key_id: Key which identifies the contacts. This can be a field
        id, id or uid. If left empty, the internal ID will be used by default.
        :param key_values: List of values of the key_id to look for.
        :param fields: List of fields which defines which system fields to
        include in the output.
        :return: Values of specified fields for contacts.

        Examples:
        If you want to get the first names and last names of two users which
        emails are respectively squirrel1@squirrelmail.com and
        squirrel2@squirrelmail.com:

        >>> client.contacts.get_data(
        ...     3,
        ...     ['squirrel1@squirrelmail.com', 'squirrel2@squirrelmail.com'],
        ...     [1, 2]
        ... )
        {
            'data': {
                'errors': [],
                'result': [
                    {
                        '1': 'Donald',
                        '2': 'Trump',
                        'id': '589058827',
                        'uid': 'g8XS7T1weS'
                    },
                    {
                        '1': 'Barack',
                        '2': 'Obama',
                        'id': '589058576',
                        'uid': 'g8XS7T1weS'
                    }
                ]
            },
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'getdata')
        payload = {
            'keyId': key_id,
            'keyValues': key_values,
        }

        if fields:
            payload['fields'] = fields

        return self.connection.make_call(
            'POST',
            query_endpoint,
            payload=payload
        )

    def get_history(self,
                    contacts,
                    start_date=None,
                    end_date=None):
        """
        Returns a list of email campaign launch data for specified contacts,
        can also be restricted to specified timeframe (optional).
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/email-history/

        :param contacts: List of contact IDs to include.
        :param start_date: yyyy-mm-dd formatted date string used to filter
        emails by the date the launch was initiated.
        :param end_date: yyyy-mm-dd formatted date string used to filter
        emails by the date the launch completed.
        :return: List of email campaign launch data.

        Examples:
        If you want to get the history for contacts with ids 589058827 and
        589058576 for campaigns which started on or after the '2016-11-24':

        >>> client.contacts.get_history(
        ...     [589058827, 589058576],
        ...     start_date='2016-11-24'
        ... )
        {
            'data': [
                {
                    'bounce_status': '',
                    'contactId': '589058827',
                    'delivery_status': 'prepared',
                    'emailId': 4934,
                    'launchListId': '589803',
                    'launch_date': '2017-01-16 19:30:00'
                },
                {
                    'bounce_status': '',
                    'contactId': '589058576',
                    'delivery_status': 'launched',
                    'emailId': 982,
                    'launchListId': '3',
                    'launch_date': '2016-11-24 11:57:00'
                },
                {
                    'bounce_status': '',
                    'contactId': '589058576',
                    'delivery_status': 'launched',
                    'emailId': 1815,
                    'launchListId': '4',
                    'launch_date': '2016-12-08 11:06:00'
                }
            ],
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'getcontacthistory')
        payload = {
            'contacts': contacts,
        }

        if start_date:
            payload['startDate'] = start_date

        if end_date:
            payload['endate'] = end_date

        return self.connection.make_call(
            'POST',
            query_endpoint,
            payload=payload
        )

    def get_internal_id(self,
                        field_id,
                        field_value):
        """
        Returns the internal ID of a contact based on a specified field ID.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/fetch-internal-id/

        :param field_id: ID of the field to use.
        :param field_value: Field value to use in the query.
        :return: Internal ID of the corresponding contact.

        Examples:
        If you want to get the internal id of a contact which email is
        squirrel1@squirrelmail.com:
        >>> client.contacts.get_internal_id(
        ...     3,
        ...     'squirrel1@squirrelmail.com'
        ... )
        {'data': {'id': '589058827'}, 'replyCode': 0, 'replyText': 'OK'}
        """
        params = {
            field_id: field_value,
        }

        return self.connection.make_call(
            'GET',
            self.endpoint,
            params=params
        )

    def check_ids(self,
                  key_id,
                  key_values,
                  accept_duplicated_values=None):
        """
        Generates a list of existing contacts and errors indexed by a
        specified key ID.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/check-internal-ids/

        :param key_id: Key which identifies the contacts. This can be a field
        id, id or uid. If left empty, the internal ID will be used by default.
        :param key_values: Values specified in the key_id for those
        contacts whose internal IDs the customer wants to receive.
        :param accept_duplicated_values: All contacts' IDs are listed in the
        case of value duplication.
        :return: List of existing contacts. Errors are collected if the key_id
        is invalid, if no contact is found or if more than one contact is found
        with the same key_id value.

        Examples:
        If you want to get the internal ids of all the users with Opt-in set
        to False:
        >>> client.contacts.check_ids(31, [2], accept_duplicated_values=True)
        {
            'data': {'errors': [], 'ids': {'1': ['589058827', '589058576']}},
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'checkids')

        payload = {
            'key_id': key_id,
            'external_ids': key_values,
        }

        if accept_duplicated_values:
            payload['get_multiple_ids'] = accept_duplicated_values

        return self.connection.make_call(
            'POST',
            query_endpoint,
            payload=payload
        )

    def update(self,
               contact,
               key_id=None,
               source_id=None,
               upsert=False):
        """
        Updates a single contact using their external ID as reference, or it
        creates the contact if it does not exist in the database. Please note
        that single and multiple contact updating are combined in the demo
        page and can’t be tested separately.
        Note: Read-only fields, which are listed in System Fields, cannot be
        updated.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/update-contacts/

        :param contact: Key-value pairs which identify the contact fields
        which will be updated.
        :param key_id: Key which identifies the contacts.
        :param source_id: ID assigned to a customer’s external application,
        and is used to identify contacts created or modified by the external
        (3rd party) applications, [source_id].
        :param upsert: When enabled, if the contact does not exist in the
        database, it is created automatically.
        :return: The ID of the updated contact.

        Examples:
        If you want to update the Opt-in field to False for the user which
        internal id is 589058827:
        >>> client.contacts.update({'id': 589058827, 31: 2}, 'id')
        {'data': {'id': '589058827'}, 'replyCode': 0, 'replyText': 'OK'}

        If you want to update the Opt-in field to True for the user which
        email is squirrel1@squirrelmail.com:
        >>> client.contacts.update({3: 'squirrel1@squirrelmail.com', 31: 1}, 3)
        {'data': {'id': '589058827'}, 'replyCode': 0, 'replyText': 'OK'}
        """
        params = {}
        if upsert is True:
            params['create_if_not_exists'] = 1

        payload = dict(contact)
        if key_id:
            payload['key_id'] = key_id
        if source_id:
            payload['source_id'] = source_id

        return self.connection.make_call(
            'PUT',
            self.endpoint,
            payload=payload,
            params=params
        )

    def update_many(self,
                    key_id,
                    contacts,
                    source_id=None,
                    upsert=False):
        """
        Updates multiple contacts all at once, or upserts them if they do not
        exist in the database.
        Note: Read-only fields, which are listed in System Fields, cannot be
        updated.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/update-multiple-contacts/

        :param key_id: Key which identifies the contacts. This can be a field
        id, id, uid or eid. If left empty, the email address (field ID 3) will
        be used by default.
        :param contacts: A list of key-value pairs which uniquely identify
        the contact fields which will be created for the contact (e.g. a key
        can be the email field ID (3), and its value is the email address of
        the specific contact).
        :param source_id: ID assigned to a customer’s external application,
        and is used to identify contacts created or modified by the external
        (3rd party) applications.
        :param upsert: When True, if the contacts do not exist in the database,
        they are created automatically.
        :return: List of dictionaries with the ids of the updated contacts.

        Examples:
        If you want to update two contacts which emails are
        squirrel1@squirrelmail.com and squirrel2@squirrelmail.com to set their
        Opt-in field to False:
        >>> client.contacts.update_many(
        ...     3,
        ...     [
        ...         {3: 'squirrel1@squirrelmail.com', 31: 2},
        ...         {3: 'squirrel2@squirrelmail.com', 31: 2}
        ...     ]
        ... )
        {
            'data': {'ids': ['589058827', '589058576']},
            'replyCode': 0,
            'replyText': 'OK'
        }
        """
        params = {}
        if upsert is True:
            params['create_if_not_exists'] = 1

        payload = {
            'key_id': key_id,
            'contacts': contacts,
        }
        if source_id:
            payload['source_id'] = source_id

        return self.connection.make_call(
            'PUT',
            self.endpoint,
            payload=payload,
            params=params
        )

    def delete(self,
               contact,
               key_id=None):
        """
        Deletes a contact.
        http://documentation.emarsys.com/resource/developers/endpoints/contacts/delete-contact/

        :param contact: Key-value pairs which uniquely identify the contact,
        e.g. a key can be the email field ID (3), and its value is the email
        address of the specific contact.
        :param key_id: Key which identifies the contact. This can be a field
        id, id, uid or eid. If left empty, the email address (field ID 3) will
        be used by default.
        :return: Empty string.

        Examples:
        If you want to delete the contact which email is
        squirrel1@squirrelmail.com:
        >>> client.contacts.delete({3: 'squirrel1@squirrelmail.com'})
        {'data': '', 'replyCode': 0, 'replyText': 'OK'}
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'delete')
        payload = dict(contact)

        if key_id:
            payload['key_id'] = key_id

        return self.connection.make_call(
            'POST',
            query_endpoint,
            payload=payload
        )
