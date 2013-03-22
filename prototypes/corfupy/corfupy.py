#!/usr/bin/python
# -*- coding: utf-8 -*-

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

def naive_most_used_word(filename):
	lines = [line.strip() for line in open(filename)]
	words = flatten(map(lambda line: line.split(), lines))
	counter = collections.Counter(words)
	print (counter.most_common())

if __name__ == "__main__":
	"""CORFU reconciliator tool"""
	args = sys.argv[1:]
	if (len(args) < 1):
		usage()
	else:
		naive_most_used_word(args[0])
