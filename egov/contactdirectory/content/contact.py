__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from egov.contactdirectory import contactdirectoryMessageFactory as _
from egov.contactdirectory.config import PROJECTNAME
from egov.contactdirectory.interfaces import IContact

from ftw.geo.interfaces import IGeocodableLocation

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


schema = Schema((
        StringField(
            name='organization',
            searchable = 1,
            widget = StringWidget(
                label = _(u'label_organization', default=u'Organization'))),

        StringField(
            name='gender',
            default='m',
            vocabulary=DisplayList((
                    ('m', _(u'male')),
                    ('f', _(u'female')),
                    ('', '-'))),
            widget=SelectionWidget(
                label=_(u'label_gender', default=u'Gender'))),

        StringField(
            name='lastname',
            required=0,
            searchable=1,
            index=('TextIndex'),
            widget=StringWidget(
                label=_(u'label_lastname', default="Lastname"))),

        StringField(
            name='firstname',
            required=0,
            searchable=1,
            widget=StringWidget(
                label=_(u'label_firstname', default='Firstname'))),

        ComputedField(
            name='searchableMemberships',
            expression='context.getSearchableMembershipText()',
            searchable=1,
            widget=ComputedWidget(
                label=_(u'label_membership', default="Membership"))),

        ComputedField(
            name='memberships',
            expression='context.getMemberships()',
            widget=ComputedWidget(
                label=_('label_memberships', default="Memberships"),
                macro="contact_memberships")),

        TextField(
            name='address',
            searchable = 1,
            default_input_type='text/plain',
            default_output_type='text/plain',
            allowable_content_types=('text/plain', ),
            widget=TextAreaWidget(
                label=_(u'label_address', default='Address'),
                rows = 2)),

        StringField(
            name='zip',
            searchable = 1,
            widget = StringWidget(
                label=_(u'label_zip', default='Postal code'))),

        StringField(
            name='city',
            searchable=1,
            widget = StringWidget(
                label=_(u'label_city', default='City'))),

        BooleanField(
            name='showPlacemark',
            default=1,
            widget=BooleanWidget(
                visible = -1, # prevent data loss
                label=_(u'label_showplacemark', default=u'Show on map'))),

        StringField(
            name='country',
            required=True,
            searchable=False,
            languageIndependent=False,
            default='Schweiz',
            storage=AnnotationStorage(),
            widget=StringWidget(
                label=_(u'label_country', default='Country'))),

        StringField(
            name='email',
            searchable=1,
            validators=('isEmail',),
            widget=StringWidget(
                label=_(u'label_email', default='Email'))),

        StringField(
            name='phone_office',
            searchable=1,
            widget=StringWidget(
                label=_(u'label_phone_office',
                        default='Phone number (office)'))),

        StringField(
            name='phone_mobile',
            searchable=1,
            widget=StringWidget(
                label=_(u'label_phone_mobile', default='Mobile number'))),

        StringField(
            name='fax',
            searchable=1,
            widget=StringWidget(
                label=_(u'label_fax', default='Fax number'))),

        StringField(
            name='www',
            validators=('isURL',),
            widget=StringWidget(
                label=_(u'label_www', default='WWW'))),

        ImageField(
            name='image',
            schemata='Erweitert',
            sizes={'thumbnail': (175,999),},
            widget=ImageWidget(
                label=_(u'label_image', default='Image'))),

        StringField(
            name='academic_title',
            schemata='Erweitert',
            searchable = 0,
            widget=StringWidget(
                label = _(u'label_academic_title',
                          default=u'Academic title'))),

        StringField(
            name='function',
            schemata='Erweitert',
            searchable=1,
            widget=StringWidget(
                label=_(u'label_function', default=u'Function'))),

        StringField(
            name='department',
            schemata='Erweitert',
            searchable=1,
            widget=StringWidget(
                label=_(u'label_department', default=u'Department'))),

        StringField(
            name='salutation',
            schemata='Erweitert',
            searchable=1,
            widget=StringWidget(
                label=_(u'label_salutation', default=u'Salutation'))),

        TextField(
            name='text',
            required=False,
            searchable=True,
            schemata="Erweitert",
            allowable_content_types=('text/html', ),
            default_input_type='text/html',
            default_output_type='text/x-html-safe',
            widget=RichWidget(
                label=_(u'label_text', default=u'Text'),
                rows=25)),

        StringField(
            name='tel_private',
            searchable=1,
            schemata="Privatanschrift",
            widget=StringWidget(
                label=_(u'label_private_tel', default='Telefon private'))),

        TextField(
            name='address_private',
            default='',
            searchable=1,
            schemata="Privatanschrift",
            default_input_type='text/plain',
            default_output_type='text/plain',
            allowable_content_types=('text/plain', ),
            widget=TextAreaWidget(
                label = _(u'label_address', default=u'Address'),
                rows = 2)),

        StringField(
            name='zip_private',
            searchable=1,
            schemata="Privatanschrift",
            widget=StringWidget(
                label=_(u'label_private_zip', default='Postal code'))),

        StringField(
            name='city_private',
            searchable=1,
            schemata="Privatanschrift",
            widget=StringWidget(
                label=_(u'label_private_city', default='City'))),

        StringField(
            'ldap_dn',
            required=False,
            languageIndependent=True,
            widget=StringWidget(
                label=_(u"label_ldap_dn", default=u"LDAP DN"),
                description=_(u"help_ldap_dn", default=u""),
                visible={'edit': 'invisible', 'view': 'invisible'})),

        BooleanField(
            name='show_memberships',
            schemata='settings',
            default=True,
            widget=BooleanWidget(
                label=_(u'label_show_membership', default='Show membership'),
                description=_(u'help_show_membership',
                              default='Show memberships of this contact'))),
))


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

contact_schema['location'].write_permission = permissions.ManagePortal


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
        refs = refcat({"relationship": "member_to_contact", "targetUID": self.UID()})
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
        format = kwargs.get('format', None)
        if format == 'natural':
            full_name = '%s %s' % (self.getFirstname(), self.getLastname())
        else:
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


class ContactLocationAdapter(object):
    """Adapter that is able to represent the location of Contact in
    a geocodable string form.
    """
    implements(IGeocodableLocation)
    adapts(IContact)

    def __init__(self, context):
        self.context = context

    def getLocationString(self):
        """Build a geocodable location string from the Contact address
        related fields.
        """
        street = ' '.join(self.context.getAddress().strip().split())
        # Remove Postfach from street, otherwise Google geocoder API will
        # return wrong results
        street = street.replace('Postfach', '').replace('\r','').strip()
        zip_code = self.context.getZip()
        city = self.context.getCity()
        country = self.context.getCountry()

        # We need at least something other than country to be defined,
        # otherwise we can't do a meaningful geocode lookup
        if not (street or zip_code or city):
            return ''

        # Concatenate only the fields with a value into the location string
        location = country
        for field in [city, zip_code, street]:
            if field.strip():
                location = "%s, %s" % (field.strip(), location)

        return location


class ValidateOrganizationOrFullname(object):
    """Validate that either an organization or a full name (first
    and last name) has been supplied.
    """
    implements(IObjectPostValidation)
    adapts(IContact)

    msg = _(u'validation_error_organisation_or_name_required',
            default=u'Either the name of the organisation or first- '
            u'and lastname of the person is required.')

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
