## Script (Python) "alphabetical_title"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Provide normalized title for alphabetical search on contacts
##
from Products.CMFCore.utils import getToolByName
plone_tool = getToolByName(context, 'plone_utils', None)

if hasattr(context, 'Title'):
    a_title = context.Title()
    a_title = plone_tool.normalizeString(a_title)
    
    a_title = a_title.replace("-", "")
    a_title = a_title.replace("_", "")
    
    return a_title
