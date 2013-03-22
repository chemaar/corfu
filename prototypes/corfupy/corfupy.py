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


def usage():
	#script = __getScriptPath()
	print """Usage: 
    %s file

        file    : Company names

examples: python corfupy.py oracle-suppliers """ 
	sys.exit(-1)

def run(filename):
	lines = [line.strip() for line in open(filename)]
	#splitting = map(lambda line: line.split(), lines)
	#words = list(itertools.chain(splitting))
	#counter = collections.Counter(words)
	#print (counter.most_common())

if __name__ == "__main__":
	"""CORFU reconciliator tool"""
	args = sys.argv[1:]
	if (len(args) < 1):
		usage()
	else:
		run(args[0])
