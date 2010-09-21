from zope.i18nmessageid import MessageFactory
from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import setDefaultRoles

from Products.PlacelessTranslationService.utility import PTSTranslationDomain
from config import PROJECTNAME, product_globals, ADD_PERMISSIONS
contactdirectoryMessageFactory = MessageFactory('egov.contactdirectory')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    import content.contact
    import content.member

    content_types, constructors, ftis = atapi.process_types(
         atapi.listTypes(PROJECTNAME),
         PROJECTNAME)
    for atype, constructor in zip(content_types, constructors):
         utils.ContentInit("%s: %s" % (PROJECTNAME, atype.portal_type),
             content_types      = (atype,),
             permission         = ADD_PERMISSIONS[atype.portal_type],
             extra_constructors = (constructor,),
             ).initialize(context)
