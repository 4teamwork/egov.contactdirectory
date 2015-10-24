from egov.contactdirectory import contactdirectoryMessageFactory as _
from egov.contactdirectory.browser.helper import icon
from egov.contactdirectory.vcard import generateVCard
from egov.contactdirectory.interfaces import IContactFolderView
from ftw.tabbedview.browser import listing
from ftw.table.basesource import BaseTableSource
from ftw.table.interfaces import ITableSourceConfig, ITableSource
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from ftw.contentpage.browser.textblock_view import TextBlockView
from zope.component import adapts, getUtility
from zope.interface import implements, Interface


class ContactFolderView(BrowserView):
    """
    """
    implements(IContactFolderView)

    def list_contacts(self):
        catalog = getToolByName(self, 'portal_catalog')

        kwargs = {}
        kwargs['portal_type'] = 'Contact'
        #import pdb; pdb.set_trace()
        if self.request.has_key('SearchableText'):
            value = self.request['SearchableText']
            if len(value):
                kwargs['SearchableText'] = value + '*'
        elif self.request.has_key('alphabetical_contact_name'):
            value = self.request['alphabetical_contact_name']
            kwargs['alphabetical_title'] = value + '*'
        else:
            kwargs['SearchableText'] = ""

        results = catalog(sort_on='sortable_title',path={'query':'/'.join(self.context.getPhysicalPath()), 'depth':1}, **kwargs)
        return results

class ContactView(BrowserView):
    """Contact view for egov
    """
    def private_address(self):
        address = ""
        if self.context.getAddress_private():
            address += self.context.getAddress_private() \
                .replace('\n', '<br/>') + '<br />'

        if self.context.getAddress_private():
            address += self.context.getZip_private()
        if self.context.getAddress_private():
            address += ' ' + self.context.getCity_private()
        return address


class DownloadVCardView(BrowserView):
    """Download vCard of contact
    """
    def __call__(self):
        response = self.request.response
        response.setHeader("Content-type", "text/vcard")
        filename = '%s.vcf' % self.context.Title()
        response.setHeader("Content-Disposition",
                           'inline; filename="%s"' % filename.encode('utf-8'))
        return generateVCard(self.context).getvalue()

class MemberView(BrowserView):
    """
    """


class MemberBlockView(TextBlockView):
    """
    """

    @property
    def has_contact(self):
        return bool(self.context.getContact())

    def has_image(self):
        #check for a 'image' field in schemata
        contact = self.context.getContact()
        if contact:
            return bool(contact.getField('image').get(contact))
        return False

    def get_image_width(self):
        scale = self.get_image_scale()
        return scale.width

    def get_image_scale(self):
        contact = self.context.getContact()
        scaling = contact.restrictedTraverse('@@images')
        return scaling.scale('image', scale="thumbnail")


class IContactSourceConfig(ITableSourceConfig):
    """Marker interface for contact table source config.
    """


class ContactTab(listing.ListingView):
    """Special tab for contacts - lists brains and real members."""

    implements(IContactSourceConfig)

    sort_on = 'name'
    sort_order = 'reverse'

    show_selects = False
    show_menu = False

    columns = (
               {'column' : 'organization',
                'column_title' : _(u'Organization', default=u'Organization'),
                'sort_index' : 'organization',
                'transform' : icon,
                'width': 300},

               {'column' : 'name',
                'column_title' : _(u'Name', default=u'Name'),
                'sort_index' : 'name',
                'transform' : icon,
                'width': 300},

               {'column' : 'address',
                'column_title' : _(u'Address', default=u'Address'),
                'width': 300},

               {'column' : 'city',
                'column_title' : _(u'City', default=u'City'),
                'sort_index' : 'city',
                'width': 300},

              {'column' : 'phone',
               'column_title' : _(u'Phone', default=u'Phone'),
               'sort_index' : 'phone',
                'width': 120},

               {'column' : 'email',
                'column_title' : _(u'Email', default=u'Email'),
                'sort_index' : 'email',
                'width': 200},
               )

    def get_base_query(self):
        return None

#    template = ViewPageTemplateFile('contacttab.pt')


class ContactTableSource(BaseTableSource):
    implements(ITableSource)
    adapts(IContactSourceConfig, Interface)


    def validate_base_query(self, query):
        context = self.config.context
        plone_utils = getToolByName(context, 'plone_utils')
        registry = getUtility(IRegistry)
        acl_users = getToolByName(context, 'acl_users')
        results = []


        # Get members
        if registry['ftw.contactdirectory.showlocalroles']:
            for user_id in dict(context.get_local_roles()).keys():
                user = user = acl_users.getUserById(user_id)
                if user is not None:
                    name = '%s %s' % (
                        user.getProperty('lastname', user.id),
                        user.getProperty('firstname', ''))
                    results.append(
                        dict(
                            user_id = user._id,
                            name = name,
                            phone = user.getProperty('phone', ''),
                            email = user.getProperty('email',''),
                            type_class = '',
                            icon = '',
                            url = '%s/author/%s' % (
                                context.portal_url(),
                                user._id),))
        # Get contacts
        query = dict(
            portal_type='Contact',
            path='/'.join(context.getPhysicalPath()),sort_on='sortable_title')
        for brain in context.portal_catalog(query):
            obj = brain.getObject()
            type_class = 'contenttype-' + \
                          plone_utils.normalizeString(obj.portal_type)
            icon = ''
            if brain.getIcon:
                icon = '<img src="%s/%s" />' % (context.portal_url(),
                                                brain.getIcon)
            results.append(
                dict(
                    user_id = obj.id,
                    organization = obj.getOrganization(),
                    name = obj.Title(),
                    address = obj.getAddress(),
                    city = '%s %s' % (obj.getZip(), obj.getCity()), 
                    phone = obj.getPhone_office(),
                    email = obj.getEmail(),
                    url = obj.absolute_url(),
                    type_class = type_class,
                    icon = icon,
            ))
        return results

    def extend_query_with_ordering(self, results):
        if self.config.sort_on:
            sorter = lambda a, b: cmp(getattr(a, self.config.sort_on, ''),
                                      getattr(b, self.config.sort_on, ''))
            results.sort(sorter)

        if self.config.sort_on and self.config.sort_reverse:
            results.reverse()

        return results

    def extend_query_with_textfilter(self, results, text):
        if not len(text):
            return results

        if text.endswith('*'):
            text = text[:-1]

        def _search_method(item):
            # name
            if text.lower() in item.get('name','').lower():
                return True

            # actor
            if text.lower() in item.get('email', '').lower():
                return True

            # phone
            if text.lower() in item.get('phone', '').lower():
                return True

            # city
            if text.lower() in item.get('city', '').lower():
                return True

            # organization
            if text.lower() in item.get('organization', '').lower():
                return True

            # address
            if text.lower() in item.get('address', '').lower():
                return True

            return False

        results = filter(_search_method, results)

        return results

    def search_results(self, results):
        return results
