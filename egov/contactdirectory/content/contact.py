__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from zope.interface import implements

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from egov.contactdirectory.config import *
#from Products.ZugWebsite.content.zugschemas import finalizeZugSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
#from egov_schemas import classificationSchema, textSchema, maps_configuration_schema, finalize_egov_schema, QuantifiedSearchableTextMixin
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
                widget=StringWidget(i18n_domain='egov',
                                    label_msgid='egov_label_lastname',
                                    label='Lastname',
                                    description_msgid='egov_desc_nachname',
                                    description='Bitte Nachname eingeben',
                                    ),
                ),
    StringField('firstname',
                required=1,
                searchable=1,
                widget=StringWidget(i18n_domain='egov',
                                    label_msgid='egov_label_firstname',
                                    label='Firstname',
                                    description_msgid='egov_help_firstname',
                                    description='Bitte Vorname eingeben',
                                    ),
                ),
                
    ImageField('foto',
               sizes={'thumbnail': (175,999),},
               widget=ImageWidget(i18n_domain='egov',
                                  label_msgid='egov_label_foto',
                                  label='Foto',
                                  description_msgid='egov_help_foto',
                                  description='Bitte Foto eingeben',
                                  ),
               ),
    
    ComputedField('searchableMemberships',
      expression='context.getSearchableMembershipText()',
      searchable=1,
      widget = ComputedWidget(label="Memberships",
                               label_msgid = "egov_label_membership",
                               i18n_domain = "egov"),
    ),

    ComputedField('memberships',
                      expression='context.getMemberships()',
                      widget = ComputedWidget(label="Memberships",
                                               label_msgid = "egov_label_memberships",
                                               description_msgid = "egov_help_memberships",
                                               i18n_domain = "egov",
                                               macro="contact_memberships"),
                      ),

    TextField('address',
       # schemata='Kontakt',
        searchable = 1,        
        widget=TextAreaWidget(description='Bitte Adresse eingeben',
                              description_msgid='egov_help_address',
                              i18n_domain='egov',
                              label='Address',
                              label_msgid='egov_label_address',
        ),
    ),
    
    StringField('zip',
       #         schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(  label = 'Postal code',
                                        label_msgid = 'egov_label_zip',
                                        i18n_domain = 'egov',
                                        description = 'Enter the postal code',
                                        description_msgid = 'egov_help_zip',),
                   ),

    StringField('city', 
        #        schemata='Kontakt',
                searchable=1,
                widget = StringWidget(  label = 'City',
                                        label_msgid = 'egov_label_city',
                                        i18n_domain = 'egov',
                                        description = 'Enter the name of the city',
                                        description_msgid = 'egov_help_city',),
                   ),

    StringField('country',
                required = True,
                searchable = False,
                languageIndependent = False,
                default = 'Schweiz',
                storage = AnnotationStorage(),
                widget = StringWidget(label = 'Country',
                                      label_msgid = 'egov_label_country',
                                      i18n_domain = 'egov',
                                      description = 'Enter the name of the country',
                                      description_msgid = 'egov_help_country',
                                      ),
                ),

    StringField('phone_office',
          #      schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(  label = 'Phone number (office)',
                                        label_msgid = 'egov_label_phone_office',
                                        i18n_domain = 'egov',
                                        description = 'Enter the phone number',
                                        description_msgid = 'egov_help_phone_office',),
                ),
                
    StringField('phone_mobile',
        #        schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(  label = 'Mobile number',
                                        label_msgid = 'egov_label_phone_mobile',
                                        i18n_domain = 'egov',
                                        description = 'Enter the mobile number',
                                        description_msgid = 'egov_help_phone_mobile',),
                ),

    StringField('fax',
        #        schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(  label = 'Fax number',
                                        label_msgid = 'egov_label_fax',
                                        i18n_domain = 'egov',
                                        description = 'Enter the fax number',
                                        description_msgid = 'egov_help_fax',),
            
                ),

    StringField('email',
       # schemata='Kontakt',
        searchable = 1,        
        widget=StringWidget(description='Bitte E-Mailadresse eingeben',
                            description_msgid='egov_help_email',
                            i18n_domain='egov',
                            label='E-Mail',
                            label_msgid='egov_label_email',
                            ),
    ),

    StringField('www',
        schemata='settings',
        validators=('isURL',),
        widget=StringWidget(description='Bitte eine Website angeben',
                            description_msgid='egov_help_www',
                            i18n_domain='egov',
                            label='WWW',
                            label_msgid='egov_label_www',
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
                if parent.portal_type == 'ZugOrgEinheit':
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
