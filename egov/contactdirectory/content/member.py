# -*- coding: utf-8 -*-
__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from zope.interface import implements

from AccessControl import ClassSecurityInfo
#from Products.Archetypes.atapi import BaseContent, BooleanField, BooleanWidget, StringWidget
from Products.Archetypes.atapi import *
from egov.contactdirectory.config import PROJECTNAME
from egov.contactdirectory import contactdirectoryMessageFactory as _
from egov.contactdirectory.interfaces import IMember

from simplelayout.types.common.content.simplelayout_schemas import textSchema

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName


schema = Schema((
#     BooleanField('showTitle',
#                schemata='default',
#                default=0,
#                widget=BooleanWidget(description = "Show title",
#                                             description_msgid = "help_showtitle",
#                                             label = "Show Title",
#                                             label_msgid = "label_showtitle",
#                                             i18n_domain = "zug",
#                                             )),   


    ReferenceField(
        name='contact',
        required=True,
        widget = ReferenceWidget(label=_(u'label_contact_reference', default='Contact reference'),
                                 description=_(u'help_contact_reference', default='')
                                 ),
                                 
#        widget=ReferenceBrowserWidget(
#            allow_browse = False,
#            restrict_browsing_to_startup_directory=True,
#            show_results_without_query=True,
#            base_query={"portal_type": "Contact"},
#            force_close_on_insert = True, 
#            label='Mitglied',
#            label_msgid='label_mitglied',
#            i18n_domain='egov',
#        ),
        allowed_types=('Contact',),
        multiValued=0,
        relationship='member_to_contact',
        vocabulary_display_path_bound = 999999,
    ),

    StringField(
        name='function',
        searchable=1,
        widget=StringWidget(
            label=_(u'label_function', default='Function'),
        )
    ),

    BooleanField('show_address',
                schemata='default',
                default=0,
                widget=BooleanWidget(label=_(u'label_show_address', default='Show address'),
                                     description=_(u'help_show_address', 
                                                   default='Also show address on membership page of the organisation unit')
                                             ),
    ),
    
     BooleanField('show_image',
        schemata='Kontakt',
        default=1,
        widget=BooleanWidget(
            label=_(u'label_show_image', 
                default='Show Image'),
            description=_(u'help_show_image', 
                default='Also show image on membership page of the organisation unit')
            ),
     ),
    
    BooleanField('acquireAddress',
                schemata='Kontakt',
                default=0,
                widget=BooleanWidget(label=_(u'label_acquire_address', default='Acquire address'),
                                     description=_(u'help_acquire_address', default=''),
                                     helper_js = ('member_block_control.js', )
                                    ),
    ),
    TextField('address',
        schemata='Kontakt',
        widget=TextAreaWidget(label=_(u'label_address', default='Address'),
                              description=_(u'help_address', default="Please enter address"),
        ),
    ),
    
    StringField('zip',
                schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_zip', default='Postal code'),
                                      description=_(u'help_zip', default="Enter the postal code"),
                                      ),
                   ),

    StringField('city', 
                schemata='Kontakt',
                searchable=1,
                widget = StringWidget(label=_(u'label_city', default="City"),
                                      description=_(u'help_city', default="Enter the name of the city"),
                                      )
                   ),

    StringField('phone_office',
                schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_phone_office', default="Phone number (office)"),
                                      description=_(u'help_phone_office', default="Enter the phone number"),
                                      )
                ),
                
    StringField('phone_mobile',
                schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_phone_mobile', default='Mobile number'),
                                      description=_(u'help_phone_mobile', default="Enter the mobile number"),
                                      )
                ),

    StringField('fax',
                schemata='Kontakt',
                searchable = 1,
                widget = StringWidget(label=_(u'label_fax', default="Fax number"),
                                      description=_(u'help_fax', default="Enter the fax number"),
                                      )
                ),

    StringField('email',
        schemata='Kontakt',
        widget=StringWidget(label=_(u'label_email', default='E-Mail'),
                            description=_(u'help_email', default='Please enter e-Mail address'),
                            ),
    ),

    StringField('www',
        schemata='Kontakt',
        validators=('isURL',),
        widget=StringWidget(label=_(u'label_www', default='WWW'),
                            description=_(u'help_www', default='Please enter a website URL'),
                            ),
    ),
),
)


member_schema = ATContentTypeSchema.copy() + \
    schema.copy() + textSchema.copy()
member_schema['excludeFromNav'].default = True


finalizeATCTSchema(member_schema)
member_schema['description'].widget.visible = {'edit': 0, 'view': 0}
member_schema['title'].required = 0
member_schema['title'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
member_schema['text'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Member(ATDocumentBase):
    """
    """
    implements(IMember)
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    schema = member_schema

    # Methods

    security.declareProtected(View, 'Title')
    def Title(self, **kwargs):
        """We have to override Title here to handle arbitrary
        arguments since PortalFolder defines it."""
        org = ''
        try:
            org = self.getOrganization().Title()
        except:
            pass
        if self.getContact():
          contact = self.getContact()
          if contact and contact.getLastname() or contact.getFirstname():
            return '%s %s, %s %s' % (contact.getLastname(),contact.getFirstname(), self.getFunction(), org)
        else:
          return ''
        
    def getImageAltText(self):
        mtool = getToolByName(self, "portal_membership")
        mitglied = self.getContact() 
        if not mtool.checkPermission('View', mitglied):
            return ''
        if mitglied:
            return mitglied.Title()
            
    getImageCaption = getImageAltText
            
    def getAddress(self):
        if self.getAcquireAddress() and self.getContact():
            return self.getContact().getAddress()
        else:
            return self.getField("address").get(self)
        
    def getZip(self):
        if self.getAcquireAddress() and self.getContact(): 
            return self.getContact().getZip()
        else:
            return self.getField("zip").get(self)
                
    def getCity(self):
        if self.getAcquireAddress() and self.getContact(): 
            return self.getContact().getCity()
        else:
            return self.getField("city").get(self)
                    
    def getPhone_office(self):
        if self.getAcquireAddress() and self.getContact(): 
            return self.getContact().getPhone_office()
        else:
            return self.getField("phone_office").get(self)
                
    def getPhone_mobile(self):
        if self.getAcquireAddress() and self.getContact(): 
            return self.getContact().getPhone_mobile()
        else:
            return self.getField("phone_mobile").get(self)
                    
    def getFax(self):
        if self.getAcquireAddress() and self.getContact():
            return self.getContact().getFax()
        else:
            return self.getField("fax").get(self)
                    
    def getEmail(self):
        if self.getAcquireAddress() and self.getContact(): 
            return self.getContact().getEmail()
        else:
            return self.getField("email").get(self)
                
    def getWww(self):
        if self.getAcquireAddress() and self.getContact(): 
            return self.getContact().getWww()
        else:
            return self.getField("www").get(self)

#    def Title(self):
#        if self.getContact(): 
#            return self.getContact().Title()
#        else:
#            return ''
            
    def getOrganization(self):
        try:
            parent = self.aq_parent
            while parent.portal_type not in ['OrgUnit', "Plone Site"]:
                parent = parent.aq_parent
            if parent.portal_type == 'OrgUnit':
                return parent.Title()
        except: 
            return ""
    

registerType(Member, PROJECTNAME)


