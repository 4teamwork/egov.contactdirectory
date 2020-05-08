class DefaultLDAPAttributeMapper(object):

    def mapping(self):
        return {
            'o': 'organization',
            'sn': 'lastname',
            'givenName': 'firstname',
            'street': 'address',
            'postalCode': 'zip',
            'l': 'city',
            'c': 'country',
            'mail': 'email',
            'telephoneNumber': 'phone_office',
            'mobile': 'phone_mobile',
            'facsimileTelephoneNumber': 'fax',
            'department': 'department',
            'uid': 'uid',
             # spitex
             'title': 'function',
             'sAMAccountName': 'sAMAccountName'
        }

    def id(self):
        # spitex
        return 'sAMAccountName'
