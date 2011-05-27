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
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFCore.utils import getToolByName


schema = Schema((
     BooleanField(
        'showTitle',
        schemata='default',
        default=0,
        widget=BooleanWidget(
        label=_(
            u'label_show_title', 
            default='Show title'),
        description=_(
            u'help_show_title', 
            default='Show Title of member contact'))),   

    ReferenceField(
        name='contact',
        required=True,
        widget = ReferenceWidget(
            label=_(u'label_contact_reference', default='Contact reference'),
            description=_(u'help_contact_reference', default='')),                                 
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

    BooleanField(
        'show_address',
        schemata='default',
        default=0,
        widget=BooleanWidget(
            label=_(u'label_show_address', default='Show address'),
            description=_(
                u'help_show_address', 
               default='Also show address on membership page of the organisation unit'))),
    
     BooleanField(
        'show_image',
        schemata='Kontakt',
        default=1,
        widget=BooleanWidget(
            label=_(u'label_show_image', 
                default='Show Image'),
            description=_(u'help_show_image', 
                default='Also show image on membership page of the organisation unit')
            ),
     ),
    
    BooleanField(
        'acquireAddress',
        schemata='Kontakt',
        default=0,
        widget=BooleanWidget(
            label=_(u'label_acquire_address', default='Acquire address'),
            description=_(u'help_acquire_address', default=''),
            helper_js = ('member_block_control.js', ))),
            
    TextField(
        'address',
        schemata='Kontakt',
        widget=TextAreaWidget(
            label=_(u'label_address', default='Address'),
            description=_(u'help_address', default="Please enter address"))),
    
    StringField(
        'zip',
        schemata='Kontakt',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_zip', default='Postal code'),
            description=_(u'help_zip', default="Enter the postal code"))),

    StringField(
        'city', 
        schemata='Kontakt',
        searchable=1,
        widget = StringWidget(
            label=_(u'label_city', default="City"),
            description=_(
                u'help_city',
                default="Enter the name of the city"))),

    StringField(
        'phone_office',
        schemata='Kontakt',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_phone_office', default="Phone number (office)"),
            description=_(
                u'help_phone_office',
                default="Enter the phone number"))),
                
    StringField(
        'phone_mobile',
        schemata='Kontakt',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_phone_mobile', default='Mobile number'),
            description=_(
                u'help_phone_mobile',
                default="Enter the mobile number"))),

    StringField(
        'fax',
        schemata='Kontakt',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_fax', default="Fax number"),
            description=_(u'help_fax', default="Enter the fax number"))),

    StringField(
        'email',
        schemata='Kontakt',
        widget=StringWidget(
            label=_(u'label_email', default='E-Mail'),
            description=_(
                u'help_email',
                default='Please enter e-Mail address'))),

    StringField(
        'www',
        schemata='Kontakt',
        validators=('isURL',),
        widget=StringWidget(
            label=_(u'label_www', default='WWW'),
            description=_(
                u'help_www',
                default='Please enter a website URL'))),
),
)


member_schema = ATContentTypeSchema.copy() + schema.copy()
member_schema['excludeFromNav'].default = True

finalizeATCTSchema(member_schema)
member_schema['description'].widget.visible = {'edit': 0, 'view': 0}
member_schema['title'].required = 0
member_schema['title'].widget.visible = {'edit': 'visible', 'view': 'visible'}

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Member(base.ATCTContent):
    """
    """
    implements(IMember)
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    schema = member_schema

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


