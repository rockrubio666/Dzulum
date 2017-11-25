#!/usr/bin/python

import argparse
import sys
from ojs import ojs
from moodle import moodle
from crawlerHead import crawlerHead
from crawler import crawler

arg = ''



def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'URL from OJS site')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'URL from Moodle site')
	parser.add_argument('-c', '--crawlerHead', metavar='File', help = 'File with directories')	
	parser.add_argument('-C', '--Crawler', metavar='URL', help = 'Crawling site')	
	options = parser.parse_args()
	
	if len(sys.argv) == 1 :
		print parser.print_help()
		
	if not (options.ojs or options.moodle):
		print parser.print_help()
		
	elif options.crawlerHead in sys.argv and options.Crawler in sys.argv:
		print parser.print_help()

	elif options.ojs in sys.argv:
		ojs(options.ojs)
		if options.crawlerHead in sys.argv:
			crawlerHead(options.ojs,options.crawlerHead)
		elif options.Crawler in sys.argv:
			crawler(options.ojs)
	
	elif options.moodle in sys.argv:
		moodle(options.moodle)
		if options.crawlerHead in sys.argv: 
			crawlerHead(options.moodle,options.crawlerHead)
		elif options.Crawler in sys.argv:
			crawler(options.moodle)
	
	
	
		
getParams(arg)





