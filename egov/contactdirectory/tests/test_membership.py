from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from egov.contactdirectory.tests import FunctionalTestCase


class TestContactMembership(FunctionalTestCase):

    def setUp(self):
        super(TestContactMembership, self).setUp()
        self.grant('Manager')

    def _create_contact_directory(self):
        self.portal.portal_types.get('Folder').allowed_content_types = (
            'Member', 'Contact',
        )
        self.contact_directory = create(Builder('folder')
                                        .titled('Contact Direcotry'))
        self.contact = create(Builder('contact').
                              titled('Hugo Boss')
                              .within(self.contact_directory))

    @browsing
    def test_contact_membership_links_to_parent(self, browser):
        self._create_contact_directory()

        my_folder = create(Builder('folder')
                           .titled('My Folder'))
        create(Builder('member')
               .within(my_folder)
               .having(contact=self.contact)
               .having(function='Chief'))

        browser.login().open(self.contact)
        self.assertEqual(
            my_folder.absolute_url(),
            browser.find('(Chief)').attrib['href']
        )
