#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-03-21"

#http://api.linkedin.com/v1/company-search?keywords=Oracle&sort=relevance
import oauth2 as oauth
import httplib2
import time, os 
import urllib
import urllib2
import simplejson 
import json

import urlparse
import BaseHTTPServer 
from xml.etree import ElementTree as ET

# ElementTree for XML parsing: 
#		easy_install ElementTree
#		http://effbot.org/downloads#elementtree
# simplejson for JSON parsing: 
#		easy_install simplejson
#		https://github.com/simplejson/simplejson
 
consumer_key    =   'nfm8uw34piu1'
consumer_secret =   'VQ8qfOcMdyUMNwvK'

request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken?scope=r_basicprofile+r_fullprofile+r_network+rw_groups'
access_token_url =  'https://api.linkedin.com/uas/oauth/accessToken'
authorize_url =     'https://api.linkedin.com/uas/oauth/authorize'

config_file   = '.service.dat'
xml_file      = '.xml.dat'


http_status_print = BaseHTTPServer.BaseHTTPRequestHandler.responses
 

def get_auth():
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)

	try:
		filehandle = open(config_file)

	except IOError as e:
		filehandle = open(config_file,"w")
		print("We don't have a service.dat file, so we need to get access tokens!");
		content = make_request(client,request_token_url,{},"Failed to fetch request token","POST")

		request_token = dict(urlparse.parse_qsl(content))
		print "Go to the following link in your browser:"
		print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

		oauth_verifier = raw_input('What is the PIN? ')

		token = oauth.Token(request_token['oauth_token'],
		request_token['oauth_token_secret'])
		token.set_verifier(oauth_verifier)
		client = oauth.Client(consumer, token)

		content = make_request(client,access_token_url,{},"Failed to fetch access token","POST")

		access_token = dict(urlparse.parse_qsl(content))

		token = oauth.Token(
			key=access_token['oauth_token'],
			secret=access_token['oauth_token_secret'])

		client = oauth.Client(consumer, token)
		simplejson.dump(access_token,filehandle)

	else:
		config = simplejson.load(filehandle)
		if ("oauth_token" in config and "oauth_token_secret" in config):
			token = 	oauth.Token(config['oauth_token'],
	    				config['oauth_token_secret'])
			client = oauth.Client(consumer, token)
		else:
			print("We had a .service.dat file, but it didn't contain a token/secret?")
			exit()
	return client

# Simple oauth request wrapper to handle responses and exceptions
def make_request(client,url,request_headers={},error_string="Failed Request",method="GET",body=None):
	if body:
		resp,content = client.request(url, method, headers=request_headers, body=body)
	else:
		resp,content = client.request(url, method, headers=request_headers)

	if resp.status >= 200 and resp.status < 300:
		return content
	elif resp.status >= 500 and resp.status < 600:
		error_string = "Status:\n\tRuh Roh! An application error occured! HTTP 5XX response received."
		log_diagnostic_info(client,url,request_headers,method,body,resp,content,error_string)

	else:
		status_codes = {403: "\n** Status:\n\tA 403 response was received. Usually this means you have reached a throttle limit.",
						401: "\n** Status:\n\tA 401 response was received. Usually this means the OAuth signature was bad.",
						405: "\n** Status:\n\tA 405 response was received. Usually this means you used the wrong HTTP method (GET when you should POST, etc).",
						400: "\n** Status:\n\tA 400 response was received. Usually this means your request was formatted incorrectly or you added an unexpected parameter.",
						404: "\n** Status:\n\tA 404 response was received. The resource was not found."}
		if resp.status in status_codes:
			log_diagnostic_info(client,url,request_headers,method,body,resp,content,status_codes[resp.status])
		else:
			log_diagnostic_info(client,url,request_headers,method,body,resp,content,http_status_print[resp.status][1])



def get_xml():

	# In python, the easiest XML library prints most elegantly to files 
	# and not strings.  In this case we'll create a temporary file with 
	# the XML if one doesn't already exist

	try:
		filehandle = open(xml_file)
	except IOError as e:
		# fields used in all share examples 
		# these would usually be provided by you / the user
		comment_text = "Testing out the LinkedIn REST Share API with XML";
		title_text = "Survey: Social networks top hiring tool - San Francisco Business Times";
		url = "http://sanfrancisco.bizjournals.com/sanfrancisco/stories/2010/06/28/daily34.html";
		image = "http://images.bizjournals.com/travel/cityscapes/thumbs/sm_sanfrancisco.jpg";
		visibility = "anyone";

		share_element = ET.Element("share")
		comment = ET.SubElement(share_element,"comment")
		comment.text = comment_text

		content_element = ET.SubElement(share_element,"content")

		title = ET.SubElement(content_element,"title")
		title.text = title_text
		submitted_url = ET.SubElement(content_element,"submitted-url")
		submitted_url.text = url
		submitted_image_url = ET.SubElement(content_element,"submitted-image-url")
		submitted_image_url.text = image

		visibility_element = ET.SubElement(share_element,"visibility")
		code_element = ET.SubElement(visibility_element,"code")
		code_element.text = visibility

		tree = ET.ElementTree(share_element)
		tree.write(xml_file,encoding="utf-8",xml_declaration=True)
		filehandle = open(xml_file)	

	xml_content = filehandle.read()
	return xml_content


def get_json():
	comment_text = "Testing out the LinkedIn REST Share API with JSON";
	title_text = "Survey: Social networks top hiring tool - San Francisco Business Times";
	url = "http://sanfrancisco.bizjournals.com/sanfrancisco/stories/2010/06/28/daily34.html";
	image = "http://images.bizjournals.com/travel/cityscapes/thumbs/sm_sanfrancisco.jpg";
	visibility = "anyone";

	share_object = {
					"comment":comment_text,
					"content": {
						"title":title_text,
						"submitted_url":url,
						"submitted_image_url":image
					},
					"visibility": {
						"code":visibility
					}
	}

	json_content = simplejson.dumps(share_object)
	return json_content

def log_diagnostic_info(client,url,request_headers,method,body,resp,content,error_string):
	# we build up a string, then log it, as multiple calls to () are not guaranteed to be contiguous
	log = "\n\n[********************LinkedIn API Diagnostics**************************]\n\n"
	log += "\n|-> Status: " + str(resp.status) + " <-|"
	log += "\n|-> " + simplejson.dumps(error_string) + " <-|"

	log += "\n|-> Key: " + consumer_key + " <-|"
	log += "\n|-> URL: " + url + " <-|"
	log += "\n\n[*****Sent*****]\n";
	log += "\n|-> Headers:" + simplejson.dumps(request_headers) + " <-|"
	if (body):
		log += "\n|-> Body: " + body + " <-|"
	log += "\n|-> Method: " + method + " <-|"
	log += "\n\n[*****Received*****]\n"
	log += "\n|-> Response object: " + simplejson.dumps(resp) + " <-|"
	log += "\n|-> Content: " + content + " <-|";
	log += "\n\n[******************End LinkedIn API Diagnostics************************]\n\n"
	print log



if __name__ == "__main__":
	# Get authorization set up and create the OAuth client
	client = get_auth()
        print "\n********Get the company search in JSON********"
        company_name = "Oracle"
        service_url = "http://api.linkedin.com/v1/company-search"
        params = {"keywords":company_name,  "sort":"relevance", "count":"10"}
        encoded_data = urllib.urlencode(params)
        query_url = (service_url if service_url.endswith('?') else
                     '%s?' % service_url)
        request_url = query_url + encoded_data
        response = make_request(client,request_url, {"x-li-format":'json'})
        print response
        companies_json = simplejson.loads(response)
        companies = {}
        for company in companies_json['companies']['values']:
            companies[company['id']]=company['name']
        for c in companies.items():
            print c


