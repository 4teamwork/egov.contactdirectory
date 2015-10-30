from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager

class IContact(Interface):
    """
    """


class IMember(Interface):
    """
    """


class IContactFolderView(Interface):
    """
    """


class IContactListing(IViewletManager):
    """ Viewlet manager registration for contact view
    """


class ILDAPAttributeMapper(Interface):
    """
    """


class ILDAPSearch(Interface):
    """Utility for searching in LDAP.
    """
