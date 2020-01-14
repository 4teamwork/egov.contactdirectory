from unittest import TestCase
from egov.contactdirectory.testing import EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, setRoles

class ReferenceTestCase(TestCase):

    layer = EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.portal_types.get(
                    'Folder').allowed_content_types = ('Member', 'Contact')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.folder1 = self.portal.get(self.portal.invokeFactory('Folder',
            'folder1'))
        self.folder2 = self.portal.get(self.portal.invokeFactory('Folder',
            'folder2'))
        self.contact1 = self.folder1.get(self.folder1.invokeFactory('Contact', 'contact1'))
        self.contact2 = self.folder2.get(self.folder2.invokeFactory('Contact', 'contact1'))
        self.member = self.folder2.get(self.folder2.invokeFactory('Member', 'member1', contact=self.contact1.UID()))

    def test_get_membership_with_same_id(self):
        self.assertEqual(1, len(self.contact1.getMemberships()))
        self.assertEqual(self.member.UID(),
                         self.contact1.getMemberships()[0].UID(),
                         u'UIDs of expected object and Relation Source do not match'
                        )
        self.assertEqual([], self.contact2.getMemberships())
