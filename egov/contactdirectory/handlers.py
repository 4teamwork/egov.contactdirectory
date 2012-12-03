from collective.geo.settings.interfaces import IGeoCustomFeatureStyle
from zope.component import queryAdapter


def initializeCustomFeatureStyles(obj, event):
    """Initializes IGeoCustomFeatureStyle for Contacts upon object creation.

    For Contacts we want to display the map viewlet in the below content body
    viewlet, regardless of what defaults have been set the global get settings.
    """

    custom_styles = queryAdapter(obj, IGeoCustomFeatureStyle)
    custom_styles.set('use_custom_styles', True)
    custom_styles.set('map_viewlet_position', 'plone.belowcontentbody')
