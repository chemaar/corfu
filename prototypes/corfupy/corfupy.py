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
from titlecase import titlecase

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

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
    def __init__(self,   list_most_used_words = []):
        #Init sets
        self.my_stop_words=stop_company_words()
        self.stop_words_wn = stopwords.words('english') #2-Stop words from Wordnet        
        self.company_stop_words_expanded = self.expand_list_wn( self.my_stop_words)
        self.company_most_used_stop_words_expanded = self.expand_list_wn( list_most_used_words)    
        self.company_most_10_used_stop_words_expanded=Set(list_most_used_words[0:10])
     
    #Given a list of words it returns an expanded list using wordnet
    def expand_list_wn(self,  list):    
        source = Set(list)
        expanded_set = Set()
        for word in   source:
            expanded_set = expanded_set | self.create_syns_from_wn(word)
        return expanded_set |  source
    
    #Given a set of words and a name returns the name without the set of words
    def remove_set(self, set,  name): 
        token_names= word_tokenize(name)       
        filtered_token_list = [w for w in  token_names if not w in set ]
        cleaned_name = 	" ".join(["".join(filtered_token) for filtered_token in filtered_token_list])
        return cleaned_name
        
    def stop_words(self,  name):
        return self.remove_set(self.company_stop_words_expanded ,  name)
        
    def stop_and_most_words(self,  name):
        stop_unified_name = self.stop_words(name.lower())
        return self.remove_set(self.company_most_used_stop_words_expanded,  stop_unified_name)

    def fuzzy(self,  name):
        stop_unified_name = self.remove_set(self.my_stop_words ,  name.lower())
        return self.remove_set(self.company_most_10_used_stop_words_expanded,  stop_unified_name.lower())
        
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
        stop_words.append(fstop.strip().lower())
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


    
def list_most_used_words(companies):
	words = flatten(map(lambda company: company.rawname.split(), companies))
	counter = collections.Counter(words)   #FIXME: calculate with percentiles
	return [x[0].lower() for x in filter ( lambda x: x [1] > 50,  (itertools.islice(counter.most_common(), 0, 1000)))]

def unique_words(string, ignore_case=False):
    key = None
    if ignore_case:
        key = str.lower
    return " ".join(unique_everseen(string.split(), key=key))
   
if __name__ == "__main__":
   companies = create_companies()
   #companies = create_companies_from_file("/home/chema/projects/corfu/prototypes/data/suppliers-clean")
   list_most_used_words = list_most_used_words(companies)
   print "Readed "+str(len(companies))
#      #print companies_as_d3(companies)
   unifier = Unifier(list_most_used_words)
   print "Starting unification..."
   for company in companies:        
        unified_name = unifier.stop_and_most_words(company.rawname)        
        final_unified_name = titlecase(' '.join(unique_list(unified_name.split())))
        if final_unified_name:
            company.unified_names.append(Company(final_unified_name, 1))
        else:
            fuzzy_unified_name = unifier.fuzzy(company.rawname)     
            if not(fuzzy_unified_name) or len(fuzzy_unified_name) ==1:
                    company.unified_names.append(Company("Others", 1))
            else:
                final_fuzzy_unified_name = titlecase(' '.join(unique_list(fuzzy_unified_name.split()))) 
                company.unified_names.append(Company(final_fuzzy_unified_name, 1))
   print "End unification..."
   #Once the list is available we create a second level using string comparison
   #Given a list of companies add new one comparing one element with others
   #print "Total companies "+str(len(companies))
   #for company in companies:
    #    for unified_name in company.unified_names:            
     #           print company.rawname+"#"+unified_name.rawname                
     #
  #Extract all unifiednames
   choicesSet = Set()
   for company in companies:
       for unified_name in company.unified_names:            
            choicesSet.add(unified_name.rawname)
           
   choices = list(choicesSet)
   for company in companies:
       company_unified_names=Set()
       new_unified_names = Set()
       for unified_name in company.unified_names:            
            company_unified_names.add(unified_name.rawname)
            #if the confidence is 100 there is no change so no new name is added
            #if the confidence is <100 the name is added
            for name,  confidence in process.extract(unified_name.rawname, choices, limit=2):
                if confidence < 100:
                    new_unified_names.add(name)            
       print "Initial unified names "+str(len(company.unified_names))
       final_unified_names =  new_unified_names - company_unified_names 
       print "New distinct unified names "+str(len(final_unified_names))
       for i in final_unified_names:
                print "Rawname: "+company.rawname+" new unified name "+i
            
            
   print "Starting concurrences..."
   #concurrences = company_concurrences(companies)
   #print len(concurrences.items())
   print "End concurrences..."
   #print companies_as_d3(concurrences)  


