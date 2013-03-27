#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-03-21"

try:
    import json
except ImportError:
    import simplejson as json
import urllib
import urllib2

from googleplaces import GooglePlaces, GooglePlacesSearchResult,  GooglePlacesError, types, lang

#Tesear Hack : remember to change your api key
QUERY_API_URL='https://maps.googleapis.com/maps/api/place/textsearch/json'
YOUR_API_KEY = 'AIzaSyCJZXAewk6RvVH9IFQAIllQc6dbTf-ovb'

def _fetch_remote_json(service_url, params={}, use_http_post=False):
    """Retrieves a JSON object from a URL."""
    if not use_http_post:
        encoded_data = urllib.urlencode(params)
        query_url = (service_url if service_url.endswith('?') else
                     '%s?' % service_url)
        request_url = query_url + encoded_data
        request = urllib2.Request(request_url)
    else:
        request_url = service_url
        request = urllib2.Request(service_url, data=params)
    response = urllib2.urlopen(request)
    return (request_url, json.load(response))
    
def _validate_response(url, response):
    """Validates that the response from Google was successful."""
    if response['status'] not in [GooglePlaces.RESPONSE_STATUS_OK,
                                  GooglePlaces.RESPONSE_STATUS_ZERO_RESULTS]:
        error_detail = ('Request to URL %s failed with response code: %s' %
                        (url, response['status']))
        raise GooglePlacesError, error_detail
       
def _get_place_details(reference, api_key, sensor=False):
    """Gets a detailed place response.

    keyword arguments:
    reference -- The unique Google reference for the required place.
    """
    url, detail_response = _fetch_remote_json(GooglePlaces.DETAIL_API_URL,
                                              {'reference': reference,
                                               'sensor': str(sensor).lower(),
                                               'key':YOUR_API_KEY})
    _validate_response(url, detail_response)
    return detail_response['result']
        

request_params = {"key":YOUR_API_KEY,"query":"Oracle", "sensor":"false"};
 
url, places_response = _fetch_remote_json(QUERY_API_URL, request_params)
_validate_response(url, places_response)
query_result = GooglePlacesSearchResult( None, places_response)

if query_result.has_attributions:
    print query_result.html_attributions


for place in query_result.places:
    # Returned places from a query are place summaries.
    print place.name
    print place.geo_location
    print place.reference

    # The following method has to make a further API call.
    details = _get_place_details(place.reference, YOUR_API_KEY,"false")
    print "URL "+details.get("url")
    print "Website "+details.get("website")
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    #print place.details # A dict matching the JSON response from Google.
    #print place.local_phone_number
    #print place.international_phone_number
    #print place.website
    #print place.url
