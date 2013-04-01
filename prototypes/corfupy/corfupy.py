#!/usr/bin/python
# -*- coding: utf-8 -*-

#http://www.clips.ua.ac.be/pages/pattern-en
#http://pixelmonkey.org/pub/nlp-training/
#http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer
#https://github.com/seatgeek/fuzzywuzzy

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-03-21"


import os
import sys
import time
import re
import urllib
from string import Template
import string
import sparql
import getopt
import collections
import itertools
from compiler.ast import flatten
import operator
import unittest
import numpy as np
from sets import Set

import nltk as nltk
from nltk import cluster
from nltk.cluster import euclidean_distance
from nltk.corpus import stopwords
from numpy import array
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#a = ["Oracle USA", "Oracle AUS"]
#a1 = map(lambda line: line.split(), a)
#a1.sort(key=itemgetter(1))
#a2 = groupby(a1, itemgetter(1))
#for elt, items in groupby(x, itemgetter(1)):
#    print elt, items
#    for i in items:
#        print i


#things = [("animal", "bear"), ("animal", "duck"), ("plant", "cactus"), ("vehicle", "speed boat"), ("vehicle", "school bus")]
#
#for key, group in groupby(things, lambda x: x[0]):
#    for thing in group:
#        print "A %s is a %s." % (thing[1], key)
#    print " "
   
class Company:
    rawname = ""
    provider = ""
    confidence = 0
    unified_names = [] #set of Companies
    def __init__(self, rawname,  provider="Raw", confidence=0):
        self.rawname = rawname
        self.provider = provider    
        self.confidence = confidence
        self.unified_names = [] 
    def __str__(self):
        uf = ", ".join(c.rawname for c in  self.unified_names)
        return "R: "+self.rawname+" P: "+self.provider+" ("+str(self.confidence)+")"+" U: unified names: ["+uf+"]"
    
class Unifier:    
    def __init__(self):
        self.stop_words_wn = stopwords.words('english') #Stop words from Wordnet
        self.extracted_company_stop_words = stop_company_words() #Hand-made stop words 
        expanded_company_stop_words = Set()
        for word in   self.extracted_company_stop_words:
            expanded_company_stop_words = expanded_company_stop_words | self.create_syns_from_wn(word)
        self.company_stop_words = list(Set(self.stop_words_wn) | Set(self.extracted_company_stop_words) | expanded_company_stop_words)
     
    def stop_words(self,  name):
        token_names= word_tokenize(name)       
        filtered_token_list = [w for w in  token_names if not w in self.company_stop_words ]
        unified_name = 	" ".join(["".join(filtered_token) for filtered_token in filtered_token_list])
        return unified_name
        
    def create_syns_from_wn(self, word):
        syns = wn.synsets(word) 
        lemmas = Set()
        for syn in syns:
            lemmas = lemmas | Set([lemma.name for lemma in syn.lemmas] )
        return lemmas

#Test


class CorfuTester(unittest.TestCase):

    def testNaiveCorfu(self):        
        company_names = getCompanyNames()
        unified_name_expected = "Oracle Pty Corporation Australia"
        corfu_names = naive_most_used_word(company_names)

        for key, value in corfu_names.items():
            self.assertEqual(unified_name_expected,   value)
         
#Helper functions:

#FIXME: check errors
def create_companies_from_file(filename):
    raw_companies = []
    for line in open(filename):
        #rawname = filter(lambda x: x in string.printable, line)
        #Be careful removing acronyms and blank spaces!
        rawname = filter(lambda x: x in string.letters or x in string.whitespace, line)
        raw_companies.append(Company(rawname.strip(), 1)) 
    return raw_companies


def create_companies():
        companies = []
        company_names = getCompanyNames()
        for name in company_names:
            rawname = filter(lambda x: x in string.letters or x in string.whitespace, name)
            companies.append(Company(rawname.strip()))
        return companies

 
def stop_company_words():
    filename="stop-words.txt"
    stop_words = []    
    for line in open(filename):
        fstop = filter(lambda x: x in string.letters or x in " ", line)
        stop_words.append(fstop.strip())
    print stop_words
    return stop_words

def getCompanyNames():
       return  ["Oracle", 
            "Oracle Australia Pty Limited", 
            "Oracle Australia Pty Limited DO NOT", 
            "Oracle Australia Pty Ltd", 
            "Oracle Corpartion", 
            "Oracle Corp Aust P/L", 
            "Oracle Corp. Aust. P/L", 
            "Oracle Corp Aust Pty Limited", 
            "Oracle (Corp) Aust Pty Ltd", 
            "Oracle Corp (Aust) Pty Ltd", 
            "Oracle Corp Aust Pty Ltd", 
            "Oracle Corp. Australia", 
            "Oracle Corp. Australia Pty.Ltd.", 
            "Oracle Corpoartion (Aust) Pty Ltd", 
            "Oracle Corporate Aust Pty Ltd", 
            "Oracle Corporation", 
            "Oracle Corporation (Aust)", 
            "Oracle Corporation Aust", 
            "Oracle Corporation Aust P/L", 
            "Oracle Corporation Aust Pty Limited", 
            "Oracle Corporation (Aust) Pty Ltd", 
            "Oracle Corporation Aust Pty Ltd", 
            "Oracle Corporation Aust. Pty Ltd", 
            "Oracle Corporation Australia", 
            "Oracle Corporation Australia Limited", 
            "Oracle Corporation Australia P/L", 
            "Oracle Corporation Australia Pty", 
            "Oracle Corporation Australia Pty Li", 
            "Oracle Corporation Australia Pty Limited", 
            "Oracle Corporation Australia Pty lt", 
            "Oracle Corporation Australia Pty Lt", 
            "Oracle corporation Australia Pty Ltd", 
            "Oracle Corporation (Australia) Pty Ltd", 
            "Oracle Corporation Australia Pty Ltd", 
            "Oracle Corporation Australia PTY ltd", 
            "Oracle Corporation Australia PTY LTD", 
            "Oracle Corporation Ltd", 
            "Oracle Corporation Pty Ltd", 
            "Oracle Pty Limited", 
            "Oracle Risk Consultants", 
            "Oracle Systems (Aust) Pty Ltd", 
            "Oracle Systems (Aust) Pty Ltd - ACT", 
            "Oracle Systems Australia P/L", 
            "Oracle Systems (Australia) Pty Ltd", 
            "Oracle University"]

               
def cluster_test():
    vectors = [array(company) for company in getCompanyNames()]
    clusterer = cluster.KMeansClusterer(2, euclidean_distance)
    clusterer.cluster(vectors, True)
    
""" 
Given a list of companies returns an associative array:
[company_name] = unified_name
"""
def naive_most_used_word(raw_company_names):
	max_words = round(np.mean(map(lambda company_name: len(company_name.split()), raw_company_names)))
	words = flatten(map(lambda company_name: company_name.split(), raw_company_names))
	counter = collections.Counter(words)
	first_max_words_names = (itertools.islice(counter.most_common(), 0, max_words))
	unified_name = 	" ".join(["".join(name[0]) for name in 	first_max_words_names])
	return create_unified_map(raw_company_names, unified_name)

def create_unified_map(raw_company_names, unified_name):
	unified_names = {}
	for company_name in raw_company_names:
		unified_names[company_name] = unified_name
	return unified_names

""" 
Given a file with a company per line returns the list of values
"""
def naive_most_used_word_from_file(filename):
    raw_company_names = [line.strip() for line in open(filename)]
    return naive_most_used_word (raw_company_names)
	
    
    
#FIXME: save to a file and make a separate script batch process...

def company_concurrences(companies):
    company_names = {}
    #1-Calculate ocurrences
    for company in companies:
        if len(company.unified_names) > 0:
            for unified_name in company.unified_names:            
                if unified_name.rawname in company_names.keys():
                    company_names[unified_name.rawname] = company_names[unified_name.rawname] + 1
                else:
                    company_names[unified_name.rawname] =  1
        else :
            company_names[company.rawname] =  1
    return company_names
            
def companies_as_d3(concurrences):
    d3 = "{"
    d3 += "\"name\": \"flare\","    
    d3 += "\"children\": [{ "    
    d3 += "\"name\": \"cluster\","    
    d3 += "\"children\": [{ "    
    d3 += "\"name\": \"suppliers\","    
    d3 += "\"children\": [ "    
    d3 += ", ".join(["{\"name\": \"%s\" , \"size\" : %s }"%(c,str(v))  for c, v in concurrences.items()])
    d3 += "]"   
    d3 += "}]"   
    d3 += "}]"   
    d3 += "}"   
    return d3
    
if __name__ == "__main__":
   companies = create_companies()
   #companies = create_companies_from_file("/home/chema/projects/corfu/prototypes/data/suppliers-clean")
   print "Readed "+str(len(companies))
      #print companies_as_d3(companies)
   unifier = Unifier()
   print "Starting unification..."
   for company in companies:        
        unified_name = unifier.stop_words(company.rawname)
        company.unified_names.append(Company(unified_name, 1))
        print "Unification of "+company.rawname+"-->"+ unified_name      
   print "End unification..."
   print "Starting concurrences..."
   concurrences = company_concurrences(companies)
   print "End concurrences..."
   #print companies_as_d3(concurrences)  
   #list =  ["Oracle"]
   #word = ["Oracle University"]
   #print process.extract(word,  list, limit=len(list))
   
    
#FIXME: use of lowercase
   # unittest.main()
#	"""CORFU reconciliator tool"""
#	args = sys.argv[1:]
#	if (len(args) < 1):
#		usage()
#	else:
#		print naive_most_used_word(args[0])

