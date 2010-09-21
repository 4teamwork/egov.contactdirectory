__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from egov.contactdirectory.config import *
from egov.contactdirectory import contactdirectoryMessageFactory as _

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from egov.contactdirectory.interfaces import IContact

try:
    from Products.Maps.content.Location import Location, LocationSchema
    from Products.Maps.interfaces import ILocation
    MAPS_PACKAGE_PRESENT = True
except:
    MAPS_PACKAGE_PRESENT = False
    class Location:
        pass


schema = Schema((
    StringField('lastname',
                required=1,
                searchable=1,
                index = ('TextIndex'),                     
                widget=StringWidget(label=_(u'label_lastname', 
                                        default="Lastname"),
                                    description=_(u'help_lastname', 
                                        default='Please enter last name')
                                    ),
                ),
    StringField('firstname',
                required=1,
                searchable=1,
                widget=StringWidget(label=_(u'label_firstname',
                                        default='Firstname'),
                                    description_=_(u'help_firstname',
                                        default='Please enter first name')
                                    ),
                ),
                
    ImageField('foto',
               sizes={'thumbnail': (175,999),},
               widget=ImageWidget(label=_(u'label_foto',
                                      default='Image'),
                                  description=_(u'help_foto',
                                      default='Please supply an image')
                                  ),
               ),
    
    ComputedField('searchableMemberships',
      expression='context.getSearchableMembershipText()',
      searchable=1,
      widget = ComputedWidget(label=_(u'label_membership',
                                  default="Membership")
                                  ),
    ),

    ComputedField('memberships',
                      expression='context.getMemberships()',
                      widget = ComputedWidget(label=_('label_memberships', 
                                                  default="Memberships"),
                                               description=_(u"help_memberships", 
                                                   default=""),
                                               macro="contact_memberships"
                                               ),
                      ),

    TextField('address',
       # schemata='Kontakt',
        searchable = 1,        
        widget=TextAreaWidget(label=_(u'label_address', default='Address'),
                              description=_(u'help_address', default='Please enter address'),
        ),
    ),
    
    StringField('zip',
       #         schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_zip', default='Postal code'),
                                        description=_(u'help_zip', default='Enter the postal code'),
                                        )
                   ),

    StringField('city', 
        #        schemata='Kontakt',
                searchable=1,
                widget = StringWidget(label=_(u'label_city', default='City'),
                                      description=_(u'help_city', default="Enter the name of the city")
                                      )
                                      
                   ),

    StringField('country',
                required = True,
                searchable = False,
                languageIndependent = False,
                default = 'Schweiz',
                storage = AnnotationStorage(),
                widget = StringWidget(label=_(u'label_country', default='Country'),
                                      description=_(u'help_country', default="Enter the name of the country")
                                      ),
                ),

    StringField('phone_office',
          #      schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_phone_office', default='Phone number (office)'),
                                      description=_(u'help_phone_office', default='Enter the phone number')
                                        )
                ),
                
    StringField('phone_mobile',
        #        schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_phone_mobile', default='Mobile number'),
                                      description=_(u'help_phone_mobile', default='Enter the mobile number')
                                      ),
                ),

    StringField('fax',
        #        schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_fax', default='Fax number'),
                                      description=_(u'help_fax', default='Enter the fax number')
                                      )
            
                ),

    StringField('email',
       # schemata='Kontakt',
        searchable = 1,        
        widget=StringWidget(label=_(u'label_email', default='E-Mail'),
                            description=_(u'help_email', default='Please enter e-Mail address')
                            ),
    ),

    StringField('www',
        schemata='settings',
        validators=('isURL',),
        widget=StringWidget(label=_(u'label_www', default='WWW'),
                            description=_(u'help_www', default='Please enter a website URL')
                            ),
    ),

),
)


#if MAPS_PACKAGE_PRESENT:
#    schema = Schema((LocationSchema.get("geolocation").copy(), LocationSchema.get("markerIcon").copy())) + maps_configuration_schema + schema
    
contact_schema = ATContentTypeSchema.copy() + \
    schema.copy()# + textSchema.copy()

finalizeATCTSchema(contact_schema)
contact_schema.moveField(name='description',pos='bottom')
#contact_schema.moveField(name='text',after='description')
contact_schema['title'].required = 0
contact_schema['title'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
contact_schema['description'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}

contact_schema['country'].widget.visible = {'view' : 'hidden', 'edit': 'hidden'}

#if MAPS_PACKAGE_PRESENT:
#    # Hide the geolocation and markerIcon fields since we automatically calculate the location from the address
#    contact_schema['geolocation'].widget.visible = {'edit': 'invisible'}
#    contact_schema['markerIcon'].widget.visible = {'edit': 'invisible'}


#class Contact(QuantifiedSearchableTextMixin,  ATCTContent, Location):
class Contact(ATCTContent):
    """
    """
    implements(IContact)
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    schema = contact_schema

    security.declareProtected(permissions.View, 'getMemberships')
    def getMemberships(self, **kwargs):
        cat, refcat = getToolByName(self, "portal_catalog"), getToolByName(self, "reference_catalog")
        refs = refcat({"relationship": "member_to_contact", "targetId": self.id})
        uids = [i.sourceUID for i in refs]
        memberships = [b.getObject() for b in cat({"UID": uids})]
        return memberships       
        
    security.declareProtected(permissions.View, 'getSearchableMembershipText')
    def getSearchableMembershipText(self):
        memberships = self.getMemberships()
        result = ""
        for membership in memberships:
            result += " %s %s" % (membership.getOrganisation(), '')
        return result

            
    security.declareProtected(permissions.View, 'Title')
    def Title(self, **kwargs):
        """We have to override Title here to handle arbitrary
        arguments since PortalFolder defines it."""
        full_name = ''
        if self.getFirstname() == '' or self.getLastname() == '':
            return '...'
        full_name = '%s %s' % (self.getLastname(), self.getFirstname())
        return '%s' % full_name
            
    def get_orgunits(self, **kwargs):
        roles = []
        members = self.getBRefs(relationship='member_to_contact')
        for member in members:
            for i in range(1,10):
                parent = member.aq_explicit.aq_parent
                if parent.portal_type == 'OrgUnit':
                    break
                else:
                     parent = parent.aq_explicit.aq_parent     
            orgunit = parent.Title()
            link = parent.absolute_url()
            function = member.getFunction()
            phone = member.getPhone_office()
            roles.append(dict(orgunit=orgunit, link=link, function=function, phone=phone))
        return roles

    def SearchableText(self):
        orgunitinfo = ' '.join(['%s %s' % (_d['orgunit'],_d['function']) for _d in self.get_orgunits()])
        return '%s %s' % (ATCTContent.SearchableText(self),orgunitinfo)

registerType(Contact, PROJECTNAME)
