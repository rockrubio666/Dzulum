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
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'URL from OJS site')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'URL from Moodle site')
	parser.add_argument('-c', '--crawlerHead', metavar='File', help = 'File with directories')	
	parser.add_argument('-C', '--Crawler', metavar='URL', help = 'Crawling site')	
	parser.add_argument('-B', '--Bruteforce',metavar='Login,UserField,PassField,User,Password,UsersFile,PassFile,Message',help='Login = Url Login, User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-b', '--bruteFile',metavar='RequestFile,User,Password,UsersFile,PassFile,Message',help=' User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-v','--verbose', metavar='Number', help='Verbose Level 1-3', required=True)
	options = parser.parse_args()
	
	if len(sys.argv) == 1 :
		print parser.print_help()
	
	
	if int(options.verbose)	>= 4 or int(options.verbose) == 0:
		print parser.print_help()
	else:	
		if not (options.ojs or options.moodle):
			print parser.print_help()
		
		elif options.crawlerHead in sys.argv and options.Crawler in sys.argv:
			print parser.print_help()
		
		elif options.Bruteforce in sys.argv and options.bruteFile in sys.argv:
			print parser.print_help()

		elif options.ojs in sys.argv:
			ojs(options.ojs,options.verbose)
			if options.crawlerHead in sys.argv and options.Bruteforce in sys.argv: # Si tiene Crawler con peticiones Head & Fuerza Bruta
				crawlerHead(options.ojs,options.crawlerHead,options.verbose)
				for element in options.Bruteforce.split(','):
					bforce.append(element)
				if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
					single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
					doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
					usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
					pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
			
			elif options.Crawler in sys.argv and options.Bruteforce in sys.argv: # Crawler & Bruteforce
				crawler(options.ojs,options.verbose)
				for element in options.Bruteforce.split(','):
					bforce.append(element)
				if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
					single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
					doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
					usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
					pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
			
			elif options.crawlerHead in sys.argv and options.bruteFile in sys.argv:
				crawlerHead(options.ojs,options.crawlerHead,options.verbose)
				for element in options.bruteFile.split(','):
					bforce.append(element)
				checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5])
			
			elif options.Crawler in sys.argv and options.bruteFile in sys.argv:
				crawler(options.ojs,options.verbose)
				for element in options.bruteFile.split(','):
					bforce.append(element)
				checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5])
				
			elif options.Crawler in sys.argv: #Solo crawler
				crawler(options.ojs,options.verbose)
				
			elif options.Bruteforce in sys.argv: #Solo Bruteforce
				for element in options.Bruteforce.split(','):
					bforce.append(element)
				if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
					single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
					doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
					usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
					pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
			
			elif options.bruteFile in sys.argv:
				for element in options.bruteFile.split(','):
					bforce.append(element)
				checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose)
				
			elif options.crawlerHead: #Solo crawlerHead
				crawlerHead(options.ojs,options.crawlerHead,options.verbose)
				
				
#############Moodle	

		elif options.moodle in sys.argv:
			moodle(options.moodle,options.verbose)
			
			if options.crawlerHead in sys.argv and options.Bruteforce in sys.argv: # Si tiene Crawler con peticiones Head & Fuerza Bruta
				crawlerHead(options.moodle,options.crawlerHead,options.verbose)
				for element in options.Bruteforce.split(','):
					bforce.append(element)
				if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
					single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
					doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
					usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
					pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
			
			elif options.Crawler in sys.argv and options.Bruteforce in sys.argv: # Crawler & Bruteforce
				crawler(options.moodle,options.verbose)
				for element in options.Bruteforce.split(','):
					bforce.append(element)
				if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
					single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
					doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
					usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
					pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
					
			elif options.crawlerHead in sys.argv and options.bruteFile in sys.argv:
				crawlerHead(options.moodle,options.crawlerHead,options.verbose)
				for element in options.bruteFile.split(','):
					bforce.append(element)
				checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose)
			
			elif options.Crawler in sys.argv and options.bruteFile in sys.argv:
				crawler(options.moodle,options.verbose)
				for element in options.bruteFile.split(','):
					bforce.append(element)
				checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose)
				
			elif options.Crawler in sys.argv: #Solo crawler
				crawler(options.moodle,options.verbose)
				
			elif options.Bruteforce in sys.argv: #Solo Bruteforce
				for element in options.Bruteforce.split(','):
					bforce.append(element)
				if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
					single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
					doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
					usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
				elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
					pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose)
					
			elif options.bruteFile in sys.argv:
				for element in options.bruteFile.split(','):
					bforce.append(element)
				checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose)
			
			elif options.crawlerHead: #Solo crawlerHead
				crawlerHead(options.moodle,options.crawlerHead,options.verbose)
			
	
	
	
		
getParams(arg)






