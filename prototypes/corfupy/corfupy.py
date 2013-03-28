#!/usr/bin/python
# -*- coding: utf-8 -*-

#http://www.clips.ua.ac.be/pages/pattern-en
#http://pixelmonkey.org/pub/nlp-training/
#http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer
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
import sparql
import getopt
import getopt
import collections
import itertools
from compiler.ast import flatten
import operator
import unittest
import numpy as np

import nltk as nltk
from nltk import cluster
from nltk.cluster import euclidean_distance
from nltk.corpus import stopwords
from numpy import array
from nltk import pos_tag, word_tokenize

def usage():
	#script = __getScriptPath()
	print """Usage: 
    %s file

        file    : Company names

examples: python corfupy.py oracle-suppliers """ 
	sys.exit(-1)

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
	
    
class CorfuTester(unittest.TestCase):

    def testNaiveCorfu(self):        
        company_names = getCompanyNames()
        unified_name_expected = "Oracle Pty Corporation Australia"
        corfu_names = naive_most_used_word(company_names)

        for key, value in corfu_names.items():
            self.assertEqual(unified_name_expected,   value)

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

def stop_company_words():
    return [ "DO", "NOT", 
                "Aust","Aust.", "Australia", 
                "Systems", 
                 ")","(","-", ".", ",", ";", 
                 "P/L", 
                 "Consultants", 
                 "ACT", 
                "Corp","Corporation", "corporation", "Corpartion", "Corp.", "Corpoartion", "Corporate", 
                "Pty","Pty.","Pty.Ltd", "PTY", 
                "Ltd", "Limited", "ltd", "LTD", "Li", "lt", "Lt"]
                
def cluster_test():
    vectors = [array(company) for company in getCompanyNames()]
    clusterer = cluster.KMeansClusterer(2, euclidean_distance)
    clusterer.cluster(vectors, True)

if __name__ == "__main__":
    company_stop_words = stop_company_words()
    company_names = getCompanyNames()
    filtered_names = {}
    for name in  company_names:
        token_names= [word_tokenize(word) for word in [name]]
        for tokens in token_names:
            filtered_word_list = tokens[:]
            for word in tokens:
                if  word.lower in  stopwords.words('english') or word in company_stop_words :
                    filtered_word_list.remove(word)
            unified_name = 	" ".join(["".join(name_filtered) for name_filtered in filtered_word_list])
            print name +"-->"+unified_name+"-->"
            
#FIXME: use of lowercase
   # unittest.main()
#	"""CORFU reconciliator tool"""
#	args = sys.argv[1:]
#	if (len(args) < 1):
#		usage()
#	else:
#		print naive_most_used_word(args[0])

#    rawtext = open(plain_text_file).read()
 #   sentences = nltk.sent_tokenize(rawtext) # NLTK default sentence segmenter
 #   sentences = [nltk.word_tokenize(sent) for sent in sentences] # NLTK word tokenizer
  #  sentences = [nltk.pos_tag(sent) for sent in sentences] # NLTK POS tagger

