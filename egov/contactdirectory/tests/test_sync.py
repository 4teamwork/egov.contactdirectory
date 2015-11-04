from egov.contactdirectory.interfaces import IContact
from egov.contactdirectory.interfaces import ILDAPAttributeMapper
from egov.contactdirectory.interfaces import ILDAPCustomUpdater
from egov.contactdirectory.sync.sync import get_ldap_attribute_mapper
from egov.contactdirectory.sync.sync import sync_contacts
from egov.contactdirectory.testing import EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING
from egov.contactdirectory.tests.utils import get_ldif_records
from ftw.builder import Builder
from ftw.builder import create
from unittest2 import TestCase
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.component import provideUtility
from zope.component import provideAdapter
from zope.component import getGlobalSiteManager


class TestContactSynchronization(TestCase):

    layer = EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.contacts = create(Builder('folder').titled('Contacts'))

    def test_sync_creates_contacts(self):
        res = sync_contacts(self.contacts, get_ldif_records('contacts.ldif'))
        self.assertEquals(5, res['created'])
        self.assertEquals(5, len(self.contacts.objectIds()))

    def test_sync_creates_contact_with_attributes(self):
        res = sync_contacts(self.contacts, get_ldif_records('contact.ldif'))
        self.assertEquals(1, res['created'])

        contact = self.contacts['nina.mueller']
        self.assertEquals("cn=M\xc3\xbcller Nina,ou=Payroll,dc=domain, dc=net",
                          contact.getLdap_dn())
        self.assertEquals('Nina', contact.getFirstname())
        self.assertEquals('M\xc3\xbcller', contact.getLastname())
        self.assertEquals('4teamwork AG', contact.getOrganization())
        self.assertEquals('n.mueller@4teamwork.ch', contact.getEmail())
        self.assertEquals('Biel', contact.getCity())

    def test_sync_updates_contact(self):
        contact = create(Builder('contact').within(self.contacts).with_id(
            'nina.mueller').having(
            ldap_dn='cn=M\xc3\xbcller Nina,ou=Payroll,dc=domain, dc=net',
            firstname='Nina',
            lastname='Meier',
            ))
        res = sync_contacts(self.contacts, get_ldif_records('contact.ldif'))
        self.assertEquals(1, res['modified'])
        self.assertEquals('Nina', contact.getFirstname())
        self.assertEquals('M\xc3\xbcller', contact.getLastname())
        self.assertEquals('4teamwork AG', contact.getOrganization())
        self.assertEquals('n.mueller@4teamwork.ch', contact.getEmail())

    def test_sync_contact_without_changes(self):
        res = sync_contacts(self.contacts, get_ldif_records('contact.ldif'))
        res = sync_contacts(self.contacts, get_ldif_records('contact.ldif'))
        self.assertEquals(1, res['unchanged'])

    def test_sync_deletes_contact(self):
        create(Builder('contact').within(self.contacts).with_id(
            'julia.meier').having(
            ldap_dn='cn=Meier Julia,ou=Payroll,dc=domain, dc=net',
        ))
        res = sync_contacts(self.contacts, get_ldif_records('contact.ldif'))
        self.assertEquals(1, res['deleted'])
        self.assertNotIn('julia.meier', self.contacts.objectIds())


class TestLDAPAttributeMapper(TestCase):

    layer = EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING

    def test_default_mapper(self):
        mapper = get_ldap_attribute_mapper()
        self.assertEquals('uid', mapper.id())
        self.assertEquals('lastname', mapper.mapping()['sn'])

    def test_custom_mapper(self):
        class MyLDAPAttributeMapper(object):
            implements(ILDAPAttributeMapper)

            def mapping(self):
                return {'sAMAccountName': 'userid'}

            def id(self):
                return 'sAMAccountName'

        my_mapper = MyLDAPAttributeMapper()
        provideUtility(my_mapper)
        mapper = get_ldap_attribute_mapper()

        self.assertEquals('sAMAccountName', mapper.id())
        self.assertEquals('userid', mapper.mapping()['sAMAccountName'])

        # cleanup
        getGlobalSiteManager().unregisterUtility(my_mapper, ILDAPAttributeMapper)


class TestCustomUpdater(TestCase):

    layer = EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING

    class MyCustomUpdater(object):
        implements(ILDAPCustomUpdater)
        adapts(IContact, Interface)

        def __init__(self, contact, record):
            self.contact = contact
            self.record = record

        def update(self):
            self.contact.setFirstname('Tania')
            return True

    def setUp(self):
        self.portal = self.layer['portal']
        self.contacts = create(Builder('folder').titled('Contacts'))
        provideAdapter(TestCustomUpdater.MyCustomUpdater)

    def tearDown(self):
        getGlobalSiteManager().unregisterAdapter(TestCustomUpdater.MyCustomUpdater)

    def test_custom_updater_updates_field(self):
        sync_contacts(self.contacts, get_ldif_records('contact.ldif'))
        self.assertEquals('Tania', self.contacts['nina.mueller'].getFirstname())
