from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ContactsAlphabeticalSearchViewlet(ViewletBase):
    render = ViewPageTemplateFile('contacts_alphabetical_search_viewlet.pt')