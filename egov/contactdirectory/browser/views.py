from zope.interface import implements, Interface
from zope.component import adapts, getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from ftw.table.basesource import BaseTableSource
from simplelayout.types.common.browser.views import BlockView 
from ftw.tabbedview.browser import listing
from egov.contactdirectory.interfaces import IContactFolderView
from ftw.table.interfaces import ITableSourceConfig, ITableSource
from egov.contactdirectory import contactdirectoryMessageFactory as _

def linked(item, value):
    url = '#'
    if 'url' in item:
        url = item['url']

    value = value.decode('utf-8')
    link = u'<a href="%s">%s</a>' % (url, value)
    wrapper = u'<span class="linkWrapper">%s</span>' % link
    return wrapper


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
            

class MemberView(BrowserView):
    """
    """

class MemberBlockView(BlockView):
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


class IContactSourceConfig(ITableSourceConfig):
    """Marker interface for contact table source config.
    """


class ContactTab(listing.ListingView):
    """Special tab for contacts - lists brains and real members."""
    
    implements(IContactSourceConfig)
    
    sort_on = 'name'
    sort_order = 'reverse'

    columns = (
               {'column' : 'icon',
                'column_title' : _(u'Type', default=u'Type'),
                'transform' : linked},
               {'column' : 'name',
                'column_title' : _(u'Name', default=u'Name'),
                'sort_index' : 'name',
                'transform' : linked}, 
              {'column' : 'phone',
               'column_title' : _(u'Phone', default=u'Phone'),
               'sort_index' : 'phone',},
               {'column' : 'email',
                'column_title' : _(u'Email', default=u'Email'),
                'sort_index' : 'email',},
               )
    
    def get_base_query(self):
        return None

#    template = ViewPageTemplateFile('contacttab.pt')
    

class ContactTableSource(BaseTableSource):
    implements(ITableSource)
    adapts(IContactSourceConfig, Interface)


    def validate_base_query(self, query):
        context = self.config.context
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
                            icon = '',
                            url = '%s/author/%s' % (
                                context.portal_url(),
                                user._id),))        
        # Get contacts
        query = dict(
            portal_type='Contact',
            path='/'.join(context.getPhysicalPath()),)
        for brain in context.portal_catalog(query):
            obj = brain.getObject()
            results.append(
                dict(
                    user_id = obj.id,
                    name = obj.Title(),
                    phone = obj.getPhone_office(),
                    email = obj.getEmail(),
                    url = obj.absolute_url(),
                    icon = '<img src="%s/%s" />' % (context.portal_url(), brain.getIcon),
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

            return False

        results = filter(_search_method, results)

        return results

    def search_results(self, results):
        return results

