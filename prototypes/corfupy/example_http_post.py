try:
    import json
except ImportError:
    import simplejson as json
import urllib
import urllib2

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
        encoded_data = urllib.urlencode(params)
        request = urllib2.Request(service_url, encoded_data)
    response = urllib2.urlopen(request)
    return (request_url, json.load(response))

request_params = {"text":"Zurich Real Estate Netherlands BV"};
url, response = _fetch_remote_json("http://text-processing.com/api/phrases/", request_params,  True)
print url
print response
