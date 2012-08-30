from geopy import geocoders
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_hasattr
from Acquisition import aq_inner

def objectModifiedHandler(obj, event):
    """Handle IObjectModifiedEvent
    """

    quickinstaller_tool = getToolByName(obj, 'portal_quickinstaller')
    if quickinstaller_tool.isProductInstalled('Maps'):
        geocodeAddress(obj)


def geocodeAddress(obj):
    """Retrieves Geocode from an Address by querying GoogleMaps' geocoder and saves it
    """
    config = getMultiAdapter((obj, obj.REQUEST), name = "maps_configuration")

    api_key = config.googlemaps_key
    # do nothing if there is no api_key
    if not api_key:
        return

    #call event on object explcit! 
    obj = aq_inner(obj).aq_explicit

    if safe_hasattr(obj, 'getAddress') and safe_hasattr(obj, 'getZip') and safe_hasattr(obj, 'getCity'):
        # Get the address related fields' values from the object

        address = ''
        #XXX remove Postfach form street, otherwise google maps will return wrong geoinfos
        for l in obj.getAddress().split('\n'):
            if 'Postfach' not in l:
                address = address + '\n'+l
        zip = obj.getZip()
        city = obj.getCity()

        if city or zip:
            gmgeocoder = geocoders.Google(api_key)

            try:
                place, gps_coordinates = gmgeocoder.geocode(address + ' ' + zip + ' ' + city)
            except:
                try:
                    place, gps_coordinates = gmgeocoder.geocode(zip + ' ' + city)
                except:
                    try:
                        place, gps_coordinates = gmgeocoder.geocode(city)
                    except:
                        try:
                            place, gps_coordinates = gmgeocoder.geocode(zip)
                        except:
                            gps_coordinates = config.default_location

            obj.setGeolocation(gps_coordinates)
