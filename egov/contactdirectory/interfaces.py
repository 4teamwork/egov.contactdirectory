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
    """A utility that provides the mapping between LDAP attributes and
       Archetypes fields.
    """
    def mapping():
        """Returns a mapping of LDAP attibute names -> AT field names.
        """

    def id():
        """Returns the name of the LDAP attribute name used as contact id.
        """


class ILDAPCustomUpdater(Interface):
    """An adapter for updating a contact object with custom data.
       Adapts a contact object and the related ldap record.
    """
    def update():
        """Updates the adapted contact object. Returns true if the object was
           modified.
        """


class ILDAPSearch(Interface):
    """Utility for searching in LDAP.
    """
