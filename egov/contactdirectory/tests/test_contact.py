from egov.contactdirectory.testing import IS_PLONE_4_1
from egov.contactdirectory.tests import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from unittest2 import skipUnless


class TestContact(FunctionalTestCase):

    def setUp(self):
        super(TestContact, self).setUp()
        self.grant('Manager')

        ptypes = self.portal.portal_types
        ptypes.get('Folder').allowed_content_types = ('Member')

    @browsing
    def test_show_memberships_on_contact(self, browser):
        self.contact = create(Builder('contact')
                              .titled('Hugo Boss')
                              .having(show_memberships=True))

        folder = create(Builder('folder'))

        create(Builder('member')
               .within(folder)
               .having(contact=self.contact)
               .having(function='Chief'))

        browser.login().open(self.contact)

        self.assertEqual(1, len(browser.css('.memberships')))

    @browsing
    def test_do_not_show_memberships_on_contact(self, browser):
        self.contact = create(Builder('contact')
                              .titled('Hugo Boss')
                              .having(show_memberships=False))

        folder = create(Builder('folder'))

        create(Builder('member')
               .within(folder)
               .having(contact=self.contact)
               .having(function='Chief'))

        browser.login().open(self.contact)

        self.assertEqual(0, len(browser.css('.memberships')))

    @skipUnless(not IS_PLONE_4_1, 'requires plone > 4.1')
    @browsing
    def test_resolve_uid_in_contact(self, browser):
        folder = create(Builder('folder'))
        link = "<a class='internal-link' href=resolveuid/{}>Folder</a>".format(
            folder.UID())

        self.contact = create(Builder('contact')
                              .titled('Hugo Boss')
                              .having(text=link))

        browser.login().open(self.contact)

        self.assertEqual(
            folder.absolute_url(),
            browser.css('#content-core .internal-link').first.get('href'),
            'The folderurl should be resolved in the template.')
