from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from simplelayout.types.common.browser.views import BlockView 

class ContactFolderView(BrowserView):
    """
    """
    
    def list_contacts(self):
        catalog = getToolByName(self, 'portal_catalog')
        kwargs = {}
        kwargs['portal_type'] = 'Contact'
        if self.request.has_key('SearchableText'):
            value = self.request['SearchableText']
            if len(value):
                kwargs['SearchableText'] = value+'*'
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