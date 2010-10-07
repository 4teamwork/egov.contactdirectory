import logging
from Products.CMFCore.utils import getToolByName
# The profile id of your package:
PROFILE_ID = 'profile-egov.contactdirectory:default'

class Empty: pass


def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('egov.contactdirectory')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it                                                                                  
    # is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()


    title_extras = Empty()
    #title_extras.doc_attr = 'alphabetical_title'
    title_extras.index_type = 'Cosine Measure'
    title_extras.lexicon_id = 'htmltext_lexicon'

    # Specify the indexes you want, with ('index_name', 'index_type', extras)
    wanted = (('alphabetical_title', 'ZCTextIndex', title_extras),
              )
              
    indexables = []
    for name, meta_type, extras in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type, extras)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('egov_contactdirectory-default.txt') is None:
        return
    logger = context.getLogger('egov.contactdirectory')
    site = context.getSite()
    add_catalog_indexes(site, logger)
