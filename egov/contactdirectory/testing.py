from egov.contactdirectory.tests import builders
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from pkg_resources import get_distribution
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2
from zope.configuration import xmlconfig


IS_PLONE_4_1 = get_distribution('Plone').version.startswith('4.1')


class EgovContactdirectoryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import egov.contactdirectory

        xmlconfig.file('configure.zcml', egov.contactdirectory,
                       context=configurationContext)

        import ftw.geo
        import ftw.zipexport
        import collective.geo.settings
        import collective.geo.openlayers
        import collective.geo.geographer
        import collective.geo.contentlocations
        import collective.geo.kml

        xmlconfig.file('configure.zcml', ftw.geo,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', ftw.zipexport,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.settings,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.openlayers,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.geographer,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.contentlocations,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.kml,
                       context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2
        # products, using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'egov.contactdirectory')
        z2.installProduct(app, 'ftw.zipexport')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'egov.contactdirectory:default')
        applyProfile(portal, 'ftw.zipexport:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


EGOV_CONTACTDIRECTORY_FIXTURE = EgovContactdirectoryLayer()
EGOV_CONTACTDIRECTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EGOV_CONTACTDIRECTORY_FIXTURE, ),
    name="EgovContactdirectory:Integration")

EGOV_CONTACTDIRECTORY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EGOV_CONTACTDIRECTORY_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="EgovContactdirectory:Functional")
