from __future__ import absolute_import
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from egov.contactdirectory.interfaces import ILDAPSearch
from ldap.controls import SimplePagedResultsControl
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements
from zope.site.hooks import getSite
import ldap
import logging

try:
    # python-ldap 2.4
    LDAP_CONTROL_PAGED_RESULTS = ldap.CONTROL_PAGEDRESULTS
    PYTHON_LDAP_24 = True
except AttributeError:
    # python-ldap 2.3
    LDAP_CONTROL_PAGED_RESULTS = ldap.LDAP_CONTROL_PAGE_OID
    PYTHON_LDAP_24 = False

logger = logging.getLogger('egov.contactdirectory.sync')


class LDAPSearch(object):
    """Utility for searching in LDAP.

       Uses connection settings defined in LDAPUserFolder.
    """
    implements(ILDAPSearch)

    def connect(self):
        ldap_uf = self.ldap_userfolder()
        if ldap_uf is None:
            return None
        self.base_dn = ldap_uf.users_base
        return ldap_uf._delegate.connect()

    def ldap_userfolder(self):
        site = getSite()
        if site is None:
            return None

        uf = getToolByName(site, 'acl_users')
        registry = getUtility(IRegistry)
        plugin_id = registry.get('egov.contactdirectory.ldap_plugin_id')

        # No plugin id configured, try to find an ldap plugin
        if not plugin_id:
            for obj in uf.objectValues():
                if base_hasattr(obj, '_getLDAPUserFolder'):
                    return obj._getLDAPUserFolder()
            return None

        # Get ldap plugin configured in registry
        ldap_plugin = uf.unrestrictedTraverse(plugin_id, None)
        if ldap_plugin is None:
            return None
        return ldap_plugin._getLDAPUserFolder()

    def search(self, base_dn=None, scope=ldap.SCOPE_SUBTREE,
               filter='(objectClass=*)', attrs=[]):
        conn = self.connect()
        if conn is None:
            return []

        if base_dn is None:
            base_dn = self.base_dn

        # Get paged results to prevent exceeding server size limit
        page_size = 1000
        if PYTHON_LDAP_24:
            lc = SimplePagedResultsControl(size=page_size, cookie='')
        else:
            lc = SimplePagedResultsControl(LDAP_CONTROL_PAGED_RESULTS,
                                           True,
                                           (page_size, ''),)
        is_last_page = False
        results = []
        while not is_last_page:
            msgid = conn.search_ext(base_dn,
                                    scope,
                                    filter,
                                    attrs,
                                    serverctrls=[lc])
            rtype, rdata, rmsgid, serverctrls = conn.result3(msgid)
            results.extend(rdata)
            pctrls = [c for c in serverctrls
                      if c.controlType == LDAP_CONTROL_PAGED_RESULTS]
            if pctrls:
                if PYTHON_LDAP_24:
                    cookie = pctrls[0].cookie
                    if cookie:
                        lc.cookie = cookie
                    else:
                        is_last_page = True
                else:
                    cookie = pctrls[0].controlValue[1]
                    if cookie:
                        lc.controlValue[1] = cookie
                    else:
                        is_last_page = True
            else:
                is_last_page = True
                logger.warn("Server ignores paged results control (RFC 2696).")
        return results
