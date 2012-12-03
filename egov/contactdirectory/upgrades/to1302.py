from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.contentlocations.interfaces import IGeoMarkerUtility
from egov.contactdirectory.handlers import initializeCustomFeatureStyles
from egov.contactdirectory.setuphandlers import georef_settings
from ftw.upgrade import UpgradeStep
from zope.component import queryAdapter
from zope.component import queryUtility
import logging


log = logging.getLogger('egov.contactdirectory')


class MigrateContactLocations(UpgradeStep):
    """Upgrade step to correctly configure Plone Site and all Contacts for use
    with collective.geo.*.
    Makes sure all Contacts are IGeoreferenceable, migrates coordinates
    previously set with Products.Maps and sets up custom feature styles as
    needed.
    """

    def __call__(self):
        self.setup_install_profile('profile-ftw.geo:default')

        # Add portal_type 'Contact' to georeferenceable types if necessary
        georef_settings(self.portal)

        geo_marker = queryUtility(IGeoMarkerUtility)
        if not geo_marker:
            return

        # Make all Contacts IGeoreferenceable
        nb_items, bad_items = geo_marker.update(self.portal, ['Contact'], [])
        msg = u'%d objects updated, %d updates failed. %s' % (
            nb_items, len(bad_items), ','.join(bad_items))
        log.info(msg)

        # Configure and migrate all Contacts
        query = {'portal_type': 'Contact'}
        contacts = self.catalog_unrestricted_search(query, full_objects=True)

        for obj in contacts:
            # Set up custom feature styles so the map gets displayed
            # in the plone.belowcontentbody viewlet
            initializeCustomFeatureStyles(obj, None)

            # Migrate coordinates from Products.Maps to collective.geo.*
            try:
                coords = obj.geolocation
            except AttributeError:
                coords = None
                log.info("No previous location found for %s." % obj)
            if coords:
                lat, lng = coords
                geo_manager = queryAdapter(obj, IGeoManager)
                geo_manager.setCoordinates('Point', (lng, lat))
