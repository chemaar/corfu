    #!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2013-11-06"

import nltk as nltk
from nltk.corpus import wordnet as wn
import string
from sets import Set

def create_syns_from_wn(word):
    print "Expanding: "+word
    syns = wn.synsets(word) 
    lemmas = Set()
    print "Syns Found: "+str(len(syns))	
    for syn in syns:
      lemmas = lemmas | Set([lemma.name for lemma in syn.lemmas] )
    print "Returning lemmas: "+str(len(lemmas))
    return lemmas


def expand_list_wn(list):    
    source = Set(list)
    expanded_set = Set()
    for word in   source:
        expanded_set = expanded_set | create_syns_from_wn(word)
    return expanded_set |  source


def create_words_from_file(filename):
    raw_words = []
    for line in open(filename):
        #rawname = filter(lambda x: x in string.printable, line)
        #Be careful removing acronyms and blank spaces!
        #word = filter(lambda x: x in string.letters or x in string.whitespace, line)
        raw_words.append(line.strip()) 
    return raw_words

if __name__ == "__main__":
    seeds = create_words_from_file("seed-words.txt")
    print str(len(seeds))
    expand_seeds = expand_list_wn(seeds)
    print str(len(expand_seeds))
    outfile = open("seed-words-expanded.txt","w")
    for word in expand_seeds:
	outfile.write(word+"\n")
    outfile.close()


