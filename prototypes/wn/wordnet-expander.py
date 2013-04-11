#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-03-21"

from sets import Set
import sys
import getopt
import nltk as nltk
from nltk import cluster
from nltk.cluster import euclidean_distance
from nltk.corpus import stopwords
from numpy import array
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn



def create_words_from_file(filename):
    raw_words = []
    try:
        for line in open(filename):
            #rawname = filter(lambda x: x in string.letters or x in string.whitespace, line)
            raw_words.append(line.strip()) 
    except Exception, e:
            print "Error reading from file : " + str(e)
    return raw_words

def expand_list_wn(list):    
    source = Set(list)
    expanded_set = Set()
    for word in   source:
        expanded_set = expanded_set |    create_syns_from_wn(word)
    return expanded_set |  source

def create_syns_from_wn(word):
    syns = wn.synsets(word) 
    lemmas = Set()
    for syn in syns:
       lemmas = lemmas | Set([lemma.name for lemma in syn.lemmas] )
    return lemmas

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

if __name__ == "__main__":    
    args = sys.argv[1:]    
    if (len(args) < 1):
        print "Error missing filename"
    else:
        try:
            words = create_words_from_file(args[0])
            print "Initial size: "+str(len(words))
            expanded =  expand_list_wn(words)
            print "Final size: "+str(len(expanded))
            for i in expanded:
                print i
        except Exception, e:
            print "Error reading from file : " + str(e)
     


