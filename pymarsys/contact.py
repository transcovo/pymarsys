from .base_endpoint import BaseEndpoint


class Contact(BaseEndpoint):
    """
    Class representation of the Contacts endpoint.
    """
    def __init__(self, connection, endpoint='api/v2/contact/'):
        super().__init__(connection, endpoint)

    def create(self, contact, key_id=None, source_id=None):
        """
        Create a contact from a dict.
        :param contact: Key-value pairs which uniquely identify the contact
        fields which will be created for the contact (e.g. a key can be the
        email field ID (3), and its value is the email address of the specific
        contact).
        :param key_id: Key which identifies the contact.
        :param source_id: ID assigned to the customer’s application, used to
        differentiate contacts created or modified by the external
        applications.
        :return: Dictionary with the id of the created contact.
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
        :param contacts:  a list of key-value pairs which uniquely identify
        the contact fields which will be created for the contact (e.g. a key
        can be the email field ID (3), and its value is the email address of
        the specific contact).
        :param key_id: Key which identifies the contacts.
        :return: Dictionary with a list of the ids of the created contacts.
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
              return_,
              field_id_dict=None,
              limit=None,
              offset=None,
              excludeempty=None):
        """
        Generate a list of contacts with values for a specific field. For
        example, field_id 1 returns the first names of all contacts. Both the
        values and the contact IDs are returned.
        :param return_: Field ID used to generate the list.
        :param field_id_dict: Key is the field_id, the value determines if a
        contact should be returned or not, [field_value].
        :param limit: Specifies the maximum number of contacts to return.
        :param offset: Specifies an offset for pagination (like in SQL).
        :param excludeempty: If set to true, then all contacts with a null
        or empty value in the requested field are not returned. Any value
        except for true will be interpreted as false.
        :return: List of contacts.
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'query')
        params = {
            'return': return_,
        }

        for param_name in ('limit', 'offset', 'excludeempty'):
            param_value = locals()[param_name]
            if param_value is not None:
                params[param_name] = param_value

        if field_id_dict is not None:
            if len(field_id_dict) > 1:
                raise ValueError('Only one field_id is allowed.')
            (key, value), = field_id_dict.items()
            params[key] = value

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
        :param key_id: Key which identifies the contacts.
        :param key_values: Value of the keyId.
        :param fields: Define which system fields to include in the output.
        :return: Values of specified fields for contacts.
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
        :param contacts: Integer array which contains the contact IDs to
        include.
        :param start_date: yyyy-mm-dd formatted date string used to filter
        emails by the date the launch was initiated.
        :param end_date: yyyy-mm-dd formatted date string used to filter
        emails by the date the launch completed.
        :return: List of email campaign launch data.
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

    def fetch_internal_id(self,
                          key_field_id,
                          key_field_value):
        """
        Returns the internal ID of a contact based on a specified key ID.
        :param key_field_id: ID of the key field to use.
        :param key_field_value: Key field value to use in the query.
        :return: Internal ID of a contact.
        """
        params = {
            key_field_id: key_field_value,
        }

        return self.connection.make_call(
            'GET',
            self.endpoint,
            params=params
        )

    def check_ids(self,
                  key_id,
                  external_ids,
                  get_multiple_ids=None):
        """
        Generates a list of existing contacts and errors indexed by a
        specified key ID. Errors are collected if the key_id is invalid, if
        no contact is found or if more than one contact is found with the
        same key_id value.
        :param key_id: Key which identifies the contacts
        :param external_ids: Values specified in the key_id for those
        contacts whose internal IDs the customer wants to receive.
        :param get_multiple_ids: All contact IDs are listed in the case of
        external ID duplication.
        :return: List of existing contacts.
        """
        query_endpoint = '{}/{}/'.format(self.endpoint, 'checkids')

        payload = {
            'key_id': key_id,
            'external_ids': external_ids,
        }

        if get_multiple_ids:
            payload['get_multiple_ids'] = get_multiple_ids

        return self.connection.make_call(
            'POST',
            query_endpoint,
            payload=payload
        )

    def update(self,
               contact,
               key_id=None,
               source_id=None,
               create_if_not_exists=None):
        """
        Updates a single contact using their external ID as reference, or it
        creates the contact if it does not exist in the database. Please note
        that single and multiple contact updating are combined in the demo
        page and can’t be tested separately.
        Note: Read-only fields, which are listed in System Fields, cannot be
        updated.
        :param contact: Key-value pairs which identify the contact fields
        which will be updated.
        :param key_id: Key which identifies the contacts.
        :param source_id: ID assigned to a customer’s external application,
        and is used to identify contacts created or modified by the external
        (3rd party) applications, [source_id].
        :param create_if_not_exists: Part of the URI. When enabled, if the
        contact does not exist in the database, it is created automatically.
        :return: The ID of the updated contact.
        """
        if create_if_not_exists is True:
            params = {
                'create_if_not_exists': 1
            }
        else:
            params = {
                'create_if_not_exists': 0
            }

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
                    create_if_not_exists=None):
        """
        Updates multiple contacts all at once, or creates them if they do not
        exist in the database.
        Note: Read-only fields, which are listed in System Fields, cannot be
        updated.
        :param key_id: Key which identifies the contacts.
        :param contacts: List of key-value pairs which uniquely identify the
        contact fields which will be updated for the contact (e.g. a key can be
        the email field ID (3), and its value is the email address of the
        :param field_id: ID of the field
        :param source_id: ID assigned to a customer’s external application,
        and is used to identify contacts created or modified by the external
        (3rd party) applications
        :param create_if_not_exists: Part of the URI. When enabled, if the
        contact does not exist in the database, it is created automatically.
        :return: List of dictionaries with the ids of the updated contacts.
        """
        if create_if_not_exists is True:
            params = {
                'create_if_not_exists': 1
            }
        else:
            params = {
                'create_if_not_exists': 0
            }

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
        :param contact: Key-value pairs which uniquely identify the contact,
        e.g. a key can be the email field ID (3), and its value is the email
        address of the specific contact.
        :param key_id: Key which identifies the contact.
        :return: Empty string.
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
