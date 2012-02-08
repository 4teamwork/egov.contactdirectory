__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from egov.contactdirectory import contactdirectoryMessageFactory as _
from egov.contactdirectory.config import PROJECTNAME
from egov.contactdirectory.interfaces import IContact

from Products.Archetypes.atapi import Schema, AnnotationStorage, BaseContent, \
                                      BooleanField, BooleanWidget, registerType
from Products.Archetypes.atapi import StringField, ImageField, ComputedField
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import StringWidget, ImageWidget
from Products.Archetypes.atapi import ComputedWidget, TextAreaWidget, RichWidget
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.interfaces import IObjectPostValidation

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from zope.interface import implements, directlyProvides
from zope.component import adapts
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

try:
    from Products.Maps.content.Location import Location
    from Products.Maps.content.Location import LocationSchema
    MAPS_PACKAGE_PRESENT = True
except:
    MAPS_PACKAGE_PRESENT = False
    class Location:
        pass


schema = Schema((
    StringField(
        'organization',
        searchable = 1,
        widget = StringWidget(
            label = _(u'label_organization', default=u'Organization'),
            description = _(u'description_organization',
                            u'Enter the name of the organization'))),

    StringField(
        'gender',
        default = 'm',
        vocabulary=DisplayList((
            ('m',_(u'male')),
            ('f',_(u'female')),
            ('','-'))),
        widget = SelectionWidget(
            label = _(u'label_gender', default=u'Gender'),
            description = _(u'description_gender',
                            default=u'Enter the gender'))),

    StringField(
        'lastname',
        required=0,
        searchable=1,
        index = ('TextIndex'),
        widget=StringWidget(
            label=_(u'label_lastname', default="Lastname"),
            description=_(
                u'help_lastname',
                default='Please enter last name'))),

    StringField(
        'firstname',
        required=0,
        searchable=1,
        widget=StringWidget(
            label=_(u'label_firstname', default='Firstname'),
            description_=_(
                u'help_firstname',
                default='Please enter first name'))),

    ComputedField(
        'searchableMemberships',
        expression='context.getSearchableMembershipText()',
        searchable=1,
        widget = ComputedWidget(
            label=_(u'label_membership', default="Membership"))),

    ComputedField(
        'memberships',
        expression='context.getMemberships()',
        widget = ComputedWidget(
            label=_('label_memberships', default="Memberships"),
            description=_(u"help_memberships", default=""),
            macro="contact_memberships")),

    TextField(
        'address',
        searchable = 1,
        default_input_type = 'text/plain',
        default_output_type = 'text/plain',
        allowable_content_types = ('text/plain', ),
        widget=TextAreaWidget(
            label=_(u'label_address', default='Address'),
            description=_(u'help_address', default='Please enter address'),
            rows = 2,
        ),
    ),

    StringField(
        'zip',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_zip', default='Postal code'),
            description=_(u'help_zip', default='Enter the postal code'))),

    StringField(
        'city',
        searchable=1,
        widget = StringWidget(
            label=_(u'label_city', default='City'),
            description=_(
                u'help_city',
                default="Enter the name of the city"))),

    BooleanField(
        'showPlacemark',
        default=1,
        widget=BooleanWidget(
            label=_(u'label_showplacemark', default=u'Show on map'),
            description=_(u'help_showplacemark',
                          default=u'Show address on map'),
        ),
    ),
    StringField(
        'country',
        required = True,
        searchable = False,
        languageIndependent = False,
        default = 'Schweiz',
        storage = AnnotationStorage(),
        widget = StringWidget(
            label=_(u'label_country', default='Country'),
            description=_(
                u'help_country',
                default="Enter the name of the country"))),

    StringField(
        'email',
        searchable = 1,
        validators=('isEmail',),
        widget=StringWidget(
            label=_(u'label_email', default='E-Mail'),
            description=_(
                u'help_email',
                default='Please enter e-Mail address'))),

    StringField(
        'phone_office',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_phone_office', default='Phone number (office)'),
            description=_(
                u'help_phone_office',
                default='Enter the phone number'))),

    StringField(
        'phone_mobile',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_phone_mobile', default='Mobile number'),
            description=_(
                u'help_phone_mobile',
                default='Enter the mobile number'))),

    StringField(
        'fax',
        searchable = 1,
        widget = StringWidget(
            label=_(u'label_fax', default='Fax number'),
            description=_(
                u'help_fax',
                default='Enter the fax number'))),

    StringField(
        'www',
        validators=('isURL',),
        widget=StringWidget(
            label=_(u'label_www', default='WWW'),
            description=_(
                u'help_www',
                default='Please enter a website URL'))),

    ImageField(
        'image',
        schemata='Erweitert',
        sizes={'thumbnail': (175,999),},
        widget=ImageWidget(
            label=_(u'label_image', default='Image'),
            description=_(
                u'help_image',
                default='Please supply an image'))),

    StringField(
        'academic_title',
        schemata='Erweitert',
        searchable = 0,
        widget = StringWidget(
            label = _(u'label_academic_title', default=u'Academic title'),
            description = _(
                u'help_academic_title',
                u'Enter the academic title'))),

    StringField(
        'function',
        schemata='Erweitert',
        searchable = 1,
        widget = StringWidget(
            label = _(u'label_function', default=u'Function'),
            description = _(
                u'help_function',
                default=u'Enter the function'))),

    StringField(
        'department',
        schemata='Erweitert',
        searchable = 1,
        widget = StringWidget(
            label = _(u'label_department', default=u'Department'),
            description = _(u'help_department', u'Enter the department'))),

    StringField(
        'salutation',
        schemata='Erweitert',
        searchable = 1,
        widget = StringWidget(
            label = _(u'label_salutation', default=u'Salutation'),
            description = _(
                u'help_salutation',
                default=u'Enter the salutation'))),

    TextField(
        'text',
        required=False,
        searchable=True,
        schemata = "Erweitert",
        default_input_type = 'text/html',
        default_output_type = 'text/html',
        widget = RichWidget(
            label = _(u'label_text', default=u'Text'),
            rows = 25,)),

    StringField(
        'tel_private',
        searchable = 1,
        schemata = "Privatanschrift",
        widget = StringWidget(
            label=_(u'label_private_tel', default='Telefon private'),
            description=_(
                u'help_private_tel',
                default=''))),

    TextField(
        'address_private',
        default='',
        searchable=1,
        schemata = "Privatanschrift",
        default_input_type = 'text/plain',
        default_output_type = 'text/plain',
        allowable_content_types = ('text/plain', ),
        widget = TextAreaWidget(
            label = _(u'label_address', default=u'Address'),
            description = _(
                u'help_address_private',
                default=u'Enter the address'),
            rows = 2)),

    StringField(
        'zip_private',
        searchable = 1,
        schemata = "Privatanschrift",
        widget = StringWidget(
            label=_(u'label_private_zip', default='Postal code'),
            description=_(
                u'help_private_zip',
                default='Enter the postal code'))),

    StringField(
        'city_private',
        searchable=1,
        schemata = "Privatanschrift",
        widget = StringWidget(
            label=_(u'label_private_city', default='City'),
            description=_(
                u'help_private_city',
                default="Enter the name of the city"))),
))


if MAPS_PACKAGE_PRESENT:
    schema = Schema((LocationSchema.get("geolocation").copy(), LocationSchema.get("markerIcon").copy())) + schema

contact_schema = ATContentTypeSchema.copy() + \
    schema.copy()# + textSchema.copy()

finalizeATCTSchema(contact_schema)
contact_schema.moveField(name='description', pos='bottom')
#contact_schema.moveField(name='text',after='description')
contact_schema['title'].required = 0
contact_schema['title'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
contact_schema['description'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}

contact_schema['country'].widget.visible = {'view' : 'hidden', 'edit': 'hidden'}

# Hide settings schemata for non-managers
settings_fields = [contact_schema[key] for key in contact_schema.keys()
                        if contact_schema[key].schemata == 'settings']
for field in settings_fields:
    field.write_permission = permissions.ManagePortal

# Hide ownership schemata for non-managers
ownership_fields = [contact_schema[key] for key in contact_schema.keys()
                        if contact_schema[key].schemata == 'ownership']
for field in ownership_fields:
    field.write_permission = permissions.ManagePortal

# Hide date schemata for non-managers
dates_fields = [contact_schema[key] for key in contact_schema.keys()
                        if contact_schema[key].schemata == 'dates']
for field in dates_fields:
    field.write_permission = permissions.ManagePortal

contact_schema['language'].write_permission = permissions.ManagePortal
contact_schema['location'].write_permission = permissions.ManagePortal


if MAPS_PACKAGE_PRESENT:
    # Hide the geolocation and markerIcon fields since we automatically calculate the location from the address
    contact_schema['geolocation'].widget.visible = {'edit': 'invisible'}
    contact_schema['markerIcon'].widget.visible = {'edit': 'invisible'}


class Contact(ATCTContent, Location):
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
            result += " %s %s" % (membership.getOrganization(), '')
        return result


    security.declareProtected(permissions.View, 'Title')
    def Title(self, **kwargs):
        """We have to override Title here to handle arbitrary
        arguments since PortalFolder defines it."""
        full_name = ''
        if self.getFirstname() == '' or self.getLastname() == '':
            if not self.getOrganization():
                return '...'
            else:
                return self.getOrganization()
        full_name = '%s %s' % (self.getLastname(), self.getFirstname())
        return '%s' % full_name

    # def getOrganization(self):
    #     if getattr(self, 'organization', None) is not None:
    #         return self.organization
    #     else:
    #         return 'None'''

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



class ValidateOrganizationOrFullname(object):
    """Validate that either an organization or a full name (first
    and last name) has been supplied.
    """
    implements(IObjectPostValidation)
    adapts(IContact)

    msg = _(u"Geben Sie bitte entweder eine Organisation oder Vor- und Nachname an")

    def __init__(self, context):
        self.context = context

    def __call__(self, request):
        organization = request.form.get('organization', request.get('organization', None))
        firstname = request.form.get('firstname', request.get('firstname', None))
        lastname = request.form.get('lastname', request.get('lastname', None))
        if organization or (firstname and lastname):
            return None
        else:
            return {'organization': self.msg,
            'firstname': self.msg,
            'lastname': self.msg}
# Returning None means no error


def OrgUnitsVocabularyFactory(context):
    """Vocabulary factory for all OrgUnits a contact is a member of"""
    available_org_units = []
    members = context.getBRefs(relationship='member_to_contact')
    for member in members:
        for i in range(1,10):
            parent = member.aq_explicit.aq_parent
            if parent.portal_type == 'OrgUnit':
                break
            else:
                parent = parent.aq_explicit.aq_parent
        available_org_units.append(parent)

    # This turns a list of title->id pairs into a Zope 3 style vocabulary
    items = [(o.Title(), o.UID()) for o in available_org_units]
    return SimpleVocabulary.fromItems([('<Keine>', '')] + items)
    directlyProvides(OrgUnitsVocabularyFactory, IVocabularyFactory)

registerType(Contact, PROJECTNAME)
