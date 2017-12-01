#!/usr/bin/python

import argparse
import sys
from ojs import ojs
from moodle import moodle
from crawlerHead import crawlerHead
from crawler import crawler
from bruteforce import single,doubleFile,usersFile,pwdFile
from brutehttp import checkFile
arg = ''


def getParams(arg):
	bforce = []	
	pvalues = []
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-a', '--Agent',metavar='Set User Agent', help='User Agent value')
	parser.add_argument('-B', '--Bruteforce',metavar='Login,UserField,PassField,User,Password,UsersFile,PassFile,Message',help='Login = Url Login, User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-b', '--bruteFile',metavar='RequestFile,User,Password,UsersFile,PassFile,Message',help=' User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-c', '--crawlerHead', metavar='File', help = 'File with directories')	
	parser.add_argument('-C', '--Crawler', nargs='?', help = 'Crawling site')	
	parser.add_argument('-k', '--Cookie',metavar='Set Cookie', help='Cookie value')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'URL from Moodle site')
	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'URL from OJS site')
	parser.add_argument('-p','--proxy',metavar='Proxy IP,Port', help = 'Proxy')
	parser.add_argument('-v','--verbose', metavar='Number', nargs = '?',help='Verbose Level 1-3', default = 1)
	options = parser.parse_args()
	
	if len(sys.argv) == 1 :
		print parser.print_help()
	
	if options.verbose is None:
		options.verbose = 1
		
	if int(options.verbose)	>= 4 or int(options.verbose) == 0:
		print parser.print_help()
	
	if not (options.ojs or options.moodle):
		print parser.print_help()
	
	if options.crawlerHead in sys.argv and options.Crawler in sys.argv:
		print parser.print_help()
		
	if options.Bruteforce in sys.argv and options.bruteFile in sys.argv:
		print parser.print_help()
	
	if options.ojs in sys.argv:
		ojs(options.ojs,options.verbose,options.Cookie,options.Agent)	
	
	if options.moodle in sys.argv:
		moodle(options.moodle,options.verbose,options.Cookie,options.Agent)
		
	if options.Bruteforce in sys.argv:
		for element in options.Bruteforce.split(','):
			bforce.append(element)
		if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
			single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent)
		elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
			doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent)
		elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
			usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent)
		elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
			pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent)
	
	if options.bruteFile in sys.argv:
		for element in options.bruteFile.split(','):
			bforce.append(element)
		checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose,'','')
	
	if options.Crawler is None and options.moodle in sys.argv:
		crawler(options.moodle,options.verbose,'','')
	elif options.Crawler is None and options.ojs in sys.argv:
		crawler(options.ojs,options.verbose,'','')
	
	if options.crawlerHead in sys.argv and options.ojs in sys.argv:
		crawlerHead(options.ojs,options.crawlerHead,options.verbose,'','')
	elif options.crawlerHead in sys.argv and options.moodle in sys.argv:
		crawlerHead(options.moodle,options.crawlerHead,options.verbose,'','')
		
getParams(arg)






