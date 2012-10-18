from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zca
from zope.configuration import xmlconfig




class EgovContactdirectoryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import egov.contactdirectory

        xmlconfig.file('configure.zcml', egov.contactdirectory,
                       context=configurationContext)
        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2
        # products, using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'egov.contactdirectory')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'egov.contactdirectory:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


EGOV_CONTACTDIRECTORY_FIXTURE = EgovContactdirectoryLayer()
EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EGOV_CONTACTDIRECTORY_FIXTURE, ), name="EgovContactdirectory:Integration")
