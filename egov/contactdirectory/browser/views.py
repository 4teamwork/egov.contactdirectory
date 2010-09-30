from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from simplelayout.types.common.browser.views import BlockView 

from egov.contactdirectory.interfaces import IContactFolderView

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
    """
    """

class MemberView(BrowserView):
    """
    """

class MemberBlockView(BlockView):
    """
    """