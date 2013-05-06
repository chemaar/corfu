import sys
import urllib
import urllib2
import simplejson as json
DOMAIN = 'http://api.geonames.org/'
USERNAME = 'chema_ar' #enter your geonames username here

def fetchJson(method, params):
    uri = DOMAIN + '%s?%s&username=%s' % (method, urllib.urlencode(params), USERNAME)
    resource = urllib2.urlopen(uri).readlines()
    js = json.loads(resource[0])
    return js

def get(geonameId, **kwargs):
    method = 'getJSON'
    valid_kwargs = ('lang',)
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    return fetchJson(method, params)

def children(geonameId, **kwargs):
    method = 'childrenJSON'
    valid_kwargs = ('maxRows', 'lang',)
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None

def search(**kwargs):
    method = 'searchJSON'
    valid_kwargs = ('q', 'name', 'name_equals', 'name_startsWith', 'maxRows', 'startRow', 'country', 'countryBias', 'continentCode', 'adminCode1', 'adminCode2', 'adminCode3', 'featureClass', 'featureCode', 'lang', 'type', 'style', 'isNameRequired', 'tag', 'operator', 'charset',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None

def postalCodeSearch(**kwargs):
    method = 'postalCodeSearchJSON'
    valid_kwargs = ('postalcode', 'postalcode_startsWith', 'placename', 'placename_startsWith', 'maxRows', 'country', 'countryBias', 'style', 'operator', 'isReduced', 'charset',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('postalCodes' in results):
        return results['postalCodes']
    else:
        return None

def findNearbyPostalCodes(**kwargs):
    method = 'findNearbyPostalCodesJSON'
    valid_kwargs = ('postalcode', 'placename', 'maxRows', 'country', 'localCountry', 'lat', 'lng', 'radius', 'style',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('postalCodes' in results):
        return results['postalCodes']
    else:
        return None

def hierarchy(geonameId, **kwargs):
    method = 'hierarchyJSON'
    valid_kwargs = ('lang')
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None
