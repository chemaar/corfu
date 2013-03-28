#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-03-21"

import httplib2
import time, os 
import urllib
import urllib2
import simplejson 
import json

import urlparse
import BaseHTTPServer 
import xml.etree.cElementTree as ET

def _fetch_remote_xml(service_url, params={}, use_http_post=False):
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
    return (request_url, ET.fromstring(response.read()))
    
    

if __name__ == "__main__":
        company_name = "Oracle"
        service_url = "http://google.com/complete/search"
        params = {"q":company_name,  "output":"toolbar"}
        response = _fetch_remote_xml (service_url, params)
        xml = response[1]
        data = []
        for elem in xml.iter():
             result = filter(lambda x:x[0]=='data', elem.attrib.items())
             if len(result)>0:
                data.append(result[0][1])
        print data
      #FIXME: use XPATH

                 
            
