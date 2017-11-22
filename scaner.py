#!/usr/bin/python

import argparse
import sys
from ojs import ojs
from moodle import moodle

arg = ''



def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-o', '--ojs', help='URL from OJS',)
	parser.add_argument('-m','--moodle', help='URL from Moodle')
						
	options = parser.parse_args()
	
	if len(sys.argv) == 1 :
		print parser.print_help()
		
	if not (options.ojs or options.moodle):
		print parser.print_help()
		
	elif options.ojs in sys.argv:
		ojs(options.ojs)
	elif options.moodle in sys.argv:
		moodle(options.moodle)
	
	
		
getParams(arg)






