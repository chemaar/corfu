#!/usr/bin/python
# -*- coding: utf-8 -*-

#http://www.clips.ua.ac.be/pages/pattern-en
#http://pixelmonkey.org/pub/nlp-training/
#http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer
#https://github.com/seatgeek/fuzzywuzzy
#https://gist.github.com/alexbowe/879414

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-05-05"


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
from numpy import matrix
from sets import Set

import nltk as nltk
from nltk import cluster
from nltk.cluster import euclidean_distance
from nltk.corpus import stopwords
from numpy import array
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn

from fuzzywuzzy import fuzz
from fuzzywuzzy import utils
from fuzzywuzzy import process
from titlecase import titlecase
from speller import correct
from geonames import search

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
    


#A possibility is to generate the matrix only one time in which score[s1][s2] returns the scorer of s1 with s2
#the method should select all scores such as score[s1], sort and return n
#the method would be best_match(s1, limit):

def create_list_processed(choices,  processor=utils.asciidammit):
   list_processed = []
   for choice in choices:
        processed = processor(choice)
        list_processed.append(processed)
   return list_processed

def create_score_matrix(list_queries, list_processed, scorer=fuzz.WRatio):
   scores = {}
   scores["Others"] = [("Others",100)]
   for query in list_queries:
       for processed in list_processed:
              if not query in scores.keys():
                  scores[query] = []
              scores[query].append( (processed, scorer(query, processed)) )
        #Previous sort
       scores[query].sort(key=lambda x: [x[1]], reverse=True)
   return scores

def best_match(s1, limit, scores):
    #print scores[s1][:limit]
    return scores[s1][:limit]
    
def create_companies_from_file(filename):
    raw_companies = []
    for line in open(filename):
        #rawname = filter(lambda x: x in string.printable, line)
        #Be careful removing acronyms and blank spaces!
        rawname = filter(lambda x: x in string.letters or x in string.whitespace, line)
        raw_companies.append(Company(rawname.strip(), 1)) 
    return raw_companies

def list_most_used_words(companies):
	words = flatten(map(lambda company: company.rawname.split(), companies))
	counter = collections.Counter(words)   #FIXME: calculate with percentiles
	return [x[0].lower() for x in filter ( lambda x: x [1] > 50,  (itertools.islice(counter.most_common(), 0, 1000)))]


def read_words(filename):
    stop_words = []    
    for line in open(filename):
        fstop = filter(lambda x: x in string.letters or x in " ", line)
        stop_words.append(fstop.strip().lower())
    return stop_words

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
        print uf
        return "R: "+str(self.rawname)+"-> ["+uf+"]"

class Unifier2:
  def __init__(self, list_most_used_words = []):
    self.sentence_re = r'''(?x)      # set flag to allow verbose regexps
        ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
        | \w+(-\w+)*            # words with optional internal hyphens
        | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
        | \.\.\.                # ellipsis
        | [][.,;"'?():-_`]      # these are separate tokens
    '''  
    self.lemmatizer = nltk.WordNetLemmatizer()
    self.stemmer = nltk.stem.porter.PorterStemmer()
    self.grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
            NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    self.chunker = nltk.RegexpParser(self.grammar)
    self.my_stop_words= Set(read_words('stop-words.txt'))
    self.acronyms= Set(read_words('acronyms.txt'))
    self.stop_words_wn = Set(stopwords.words('english'))
    self.company_stop_words_expanded = self.expand_list_wn( self.my_stop_words)
    self.company_most_used_stop_words_expanded = self.expand_list_wn( list_most_used_words)    
    self.company_most_10_used_stop_words_expanded=Set(list_most_used_words[0:10])
    self.stopwords = (self.my_stop_words |  self.acronyms | self.stop_words_wn | self.company_stop_words_expanded  | self.company_most_used_stop_words_expanded )
    
  def unify(self,  text):
        toks = nltk.regexp_tokenize(text, self.sentence_re)
        postoks = nltk.tag.pos_tag(toks)
        tree = self.chunker.parse(postoks)
        terms = self.get_terms(tree)
        list_terms = []
        for term in terms:
            for word in term:
                list_terms.append(word)
        return " ".join(list_terms)
        
  def leaves(self, tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
        yield subtree.leaves()
        
  def normalise(self, word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = self.stemmer.stem_word(word)
    #word = self.lemmatizer.lemmatize(word)
    return word
    
  def acceptable_word(self, word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 < len(word) <= 40  and word.lower() not in (self.stopwords))
    return accepted
 
  def get_terms(self, tree):
    for leaf in self.leaves(tree):
        term = [ self.normalise(w) for w,t in leaf if self.acceptable_word(w) ]
        yield term
  
  def fuzzy(self,  name):
    stop_unified_name = self.remove_set(self.my_stop_words ,  name.lower())
    return self.remove_set(self.company_most_10_used_stop_words_expanded,  stop_unified_name.lower())

  def expand_list_wn(self,  list):    
    source = Set(list)
    expanded_set = Set()
    for word in   source:
        expanded_set = expanded_set | self.create_syns_from_wn(word)
    return expanded_set |  source
     
  def create_syns_from_wn(self, word):
    syns = wn.synsets(word) 
    lemmas = Set()
    for syn in syns:
      lemmas = lemmas | Set([lemma.name for lemma in syn.lemmas] )
    return lemmas
    
  def remove_set(self, set,  name): 
    token_names= word_tokenize(name)       
    filtered_token_list = [w for w in  token_names if not w in set ]
    cleaned_name = 	" ".join(["".join(filtered_token) for filtered_token in filtered_token_list])
    return cleaned_name

def score_companies(companies,  all_unified_names):
#Calculate the number of unified names [(Oracle, 10)]
   counter = collections.Counter(all_unified_names)  
   most_common = counter.most_common()
   most_common_list = [x[0] for x in most_common] 
   #Once the list is available we create a second level using string comparison
   print "Creating score matrix"
   score_matrix = create_score_matrix(all_unified_names, create_list_processed(all_unified_names))
   print "End Creating score matrix"
   #Given a list of companies add new one comparing one element with others
   for company in companies:
       company_unified_names=Set()
       new_unified_names = Set()
       for unified_name in company.unified_names:            
            company_unified_names.add(unified_name.rawname)            
            new_matches = best_match(unified_name.rawname,2,score_matrix)            
            for name in [item[0] for item in filter(lambda x:x[1]<100, new_matches)]: #if it is not a perfect match
                new_unified_names.add(name)            
       final_unified_names =  company_unified_names -new_unified_names   # FIXME: maybe optional
       for name in final_unified_names:
                company.unified_names.append(Company(name,"Matrix",  1))

def create_all_unified_names(companies, n):
    all_unified_names=[]
    return [company.unified_names[n].rawname for company in  companies]

if __name__ == "__main__":
   set_best_names=Set()
   companies = create_companies_from_file("/home/chema/projects/corfu/prototypes/data/suppliers-super-min")
   list_most_used_words = list_most_used_words(companies)
   unifier = Unifier2(list_most_used_words)
   for company in companies:        
        unified_name = unifier.unify(company.rawname)        
        final_unified_name = titlecase(' '.join(unique_list(unified_name.split())))
        if final_unified_name:
            company.unified_names.append(Company(final_unified_name, "NLP", 1))
        else:
            fuzzy_unified_name = unifier.fuzzy(company.rawname)     
            if not(fuzzy_unified_name) or len(fuzzy_unified_name) ==0:
                    company.unified_names.append(Company("Others", "NLP-Fuzzy", 1))    #FIXME: Special case
            else:
                final_fuzzy_unified_name = titlecase(' '.join(unique_list(fuzzy_unified_name.split()))) 
                company.unified_names.append(Company(final_fuzzy_unified_name, "NLP-Fuzzy", 1))
   print "End unification..."

 
 #    #The company has now a new list of unified names
#    #How can we select the best a final name?
#    #The final unified name is the most used in all unified names
   score_companies(companies,  create_all_unified_names(companies, 0))
   score_companies(companies,  create_all_unified_names(companies, 1))
   score_companies(companies,  create_all_unified_names(companies, 2))
   for company in companies:
       print company
   #

#   best_score = 0
#   best_name =  ""       
#   for unified_name in company.unified_names:   
#      if unified_name.rawname in most_common_list:
#         index = most_common_list.index(unified_name.rawname) 
#         current_score = most_common[index][1]
#         if current_score > best_score: #unless others but so far Others is not in the list of all unified names
#            best_score = current_score
#            best_name = most_common[index][0]
#   
       
   print str(len(set_best_names))
