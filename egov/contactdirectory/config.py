"""Common configuration constants
"""

PROJECTNAME = "egov.contactdirectory"
DEPENDENCIES = ('AddRemoveWidget',
                'DataGridField',
               )

ADD_PERMISSIONS = { 
    'Contact': 'egov.contactdirectory: Add Contact',
    'Member': 'egov.contactdirectory: Add Member',
}
    
from Products.Archetypes.public import DisplayList

try: # New CMF
    from Products.CMFCore.permissions import setDefaultRoles 
except ImportError: # Old CMF
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

# Check for Plone 2.1
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    HAS_PLONE21 = False
else:
    HAS_PLONE21 = True

product_globals = globals()


