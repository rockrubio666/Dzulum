#!/usr/bin/python

import argparse #Utilizado para generar el menu
import sys
import os
import git # Utilizado para actualizar la herramienta
from termcolor import colored
import random
from banner import *
from ojs import * 
from moodle import *
from crawlerHead import *
from crawler import *
from bruteforce import *
from brutehttp import *
from multiprocessing import Process #  Utilizado para realizar la ejecucion de los programas de forma paralela
arg = ''  
		
def getParams(arg):
	bforce = []	
	pvalues = []
	rvalues = []
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
	description=( 						# Descripcion de las opciones de la herramienta
	'''				Vulnerability scanner for Moodle and OJS
-----------------------------------------------------------------------------------------------
 * Agent: Lets to specify the User Agent use it in the requests, e.g: -a 'Thunderstruck'
 
 * Bruteforce: Tries to obtain the credentials of the site, it could be use with files like:
	Option with both individuals: /login,username,password,papu,pass123,,,'Error login'
	Option user and file with passwords: /login,username,password,papu,,,passFile,'Error login'
	Option file with users and password: /login,username,password,,pass123,usersFile,,'Error login'
	Option with both files: /login,username,password,,,usersFile,passFile,'Error Login'
	
 * Bruteforce with file: Tries to obtain the credentials of the site, this option needs a file with request and the usage is:
	Option with both individuals: reqFile,papu,pass123,,,'Error login'
	Option user and file with passwords: reqFile,papu,,,passFile,'Error login'
	Option file with users and password: reqFile,,pass123,usersFile,,'Error login'
	Option with both iles: reqFile,,,usersFile,passFile,'Error Login'
	
 * Cookie: Lets to specify the Session Cookie use it in the requests, e.g: -k 'Cuki'
 
 * Crawler: Look for possible links and javascript in the index page, e.g: -C
 
 * Crawler with head requests: Look for possible links and javascript in the index page with help of a file, e.g: -c sitesFile
 
 * Moodle: Searches elements necessaries to get the version and determine the possible vulnerabilities, e.g: -m https://example.com/moodle/
 
 * Proxy: Sends requests through proxy, e.g: -p 169.69.69.69,6969
 
 * OJS: Searches elements necessaries to get the version an determine the possible vulnerabilities, e.g: -o https://example.com/ojs/
 
 * Tor: Makes requests through Tor socks, e.g: -T
 
 * Verbose: Shows differents depuration levels, from 1 to 3, e.g: -v 3	'''),
	epilog = 'Enjoy it! ')

# Opciones de la herramienta
	parser.add_argument('-a', '--Agent',metavar='Set User Agent', help='User Agent value')
	parser.add_argument('-B', '--Bruteforce',metavar='Login,UserField,PassField,User,Password,UsersFile,PassFile,Message',help='Login = Url Login, User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-b', '--bruteFile',metavar='RequestFile,User,Password,UsersFile,PassFile,Message',help=' User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-c', '--crawlerHead', metavar='File', help = 'File with directories')	
	parser.add_argument('-C', '--Crawler', help = 'Crawling site',action='store_true')	
	parser.add_argument('-k', '--Cookie',metavar='Set Cookie', help='Cookide ID,Cookie value')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'URL from Moodle site')
	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'URL from OJS site')
	parser.add_argument('-p','--proxy',metavar='Proxy IP,Port', help = 'Proxy')
	parser.add_argument('-r','--report', metavar='Text,HTML,XML,Mail', help= 'Reports the results getting from the site')
	parser.add_argument('-t','--thread',help='Thread option',action='store_true')
	parser.add_argument('-T','--tor', help = 'Use Tor',action='store_true')
	parser.add_argument('-v','--verbose', metavar='Number', nargs = '?',help='Verbose Level 1-3', default = 1)
	options = parser.parse_args()
	
	
	if len(sys.argv) == 1 : # Para recibir mas de un argumento
		print parser.print_help()
		sys.exit(2)

	if int(options.verbose)	>= 4 or int(options.verbose) == 0: # Nivel de depuracion maximo = 3
		print parser.print_help()
		print 'Verbose level should be between 1 -3 >:v'
		sys.exit(2)
	
	if options.verbose is None: # Si no se especifica la opcion -v, se establece por defecto 1
		options.verbose = 1

	if not (options.ojs or options.moodle): # Validacion para que se realice el escaneo 
		print parser.print_help()
		print '\n *** Option OJS or Moodle is required ***'
		sys.exit(2)
		
	if options.Crawler == True and options.crawlerHead in sys.argv: # Validacion para solo usar un crawler
		print parser.print_help()
		print '\n *** You can only execute one Crawler a time :,v ***'
		sys.exit(2)
	
	if options.Bruteforce in sys.argv and options.bruteFile in sys.argv: # Validacion para solo usar un bruteforce
		print parser.print_help()
		print '\n *** You can only execute one Bruteforce a time :,v ***'
		sys.exit(2)
	
	if options.proxy in sys.argv and options.tor == True: # Validacion para solo usar proxy o tor
		print parser.print_help()
		print '\n You can only use one proxy a time :,v ***'
		sys.exit(2)	
	
	th = []
	if options.thread == True:
		for element in sys.argv:
			if '-C' in element:
				thC = raw_input('Number of threads for Crawler: ')
				if len(thC) < 1:
					thC = 0
					th.append(thC)
				else:
					th.append(thC)
				
			elif '-c' in element:
				thc = raw_input('Number of threads for Crawler: ')
				if len(thc) < 1:
					thc = 0
				else:
					th.append(thc)
			elif '-o' in element:
				tho = raw_input('Number of threads for OJS: ')
				if len(tho) < 1:
					tho = 0
				else:
					th.append(tho)
			elif '-m' in element:
				thm = raw_input('Number of threads for Moodle: ')
				if len(thm) < 1:
					thm = 0
				else:
					th.append(thm)
			elif '-b' in element:
				thb = raw_input('Number of threads for Bruteforce: ')
				if len(thb) < 1:
					thb = 0
				else:
					th.append(thb)
			elif '-B' in element:
				thB = raw_input('Number of threads for Bruteforce: ')
				if len(thB) < 1:
					thB = 0
				else:
					th.append(thB)	
			else:
				pass
			
		
		for element in th:
			if element.isdigit():
				pass
			else:
				print colored('The value: ','yellow') + colored(element,'red') + colored(' isn\'t a number, please check it and try again','yellow')
				sys.exit(2)
			if int(element) >= 0 and int(element) < 15:
				pass
			else:
				print colored('Please introduce a number between 0 and 15', 'yellow')
				sys.exit(2)
	else:
		tho = None
		thB = None
		thb = None
		thc = None
		thm = None
		thC = None
	
		
	if len(sys.argv) >= 3:
			numMeme = random.randint(0,5)
			numColor = random.randint(0,6)
			ban(numMeme,numColor)
			# Actualizacion de la herramienta
			update = raw_input('Do yo want to update the databases? [y/N] ') or 'N'
			if 'Y' in update or 'y' in update:
				cwd = os.getcwd()		
				g = git.cmd.Git(cwd)
				g.pull()
				print 'Databases Updated :D'
			else:
				print 'No updated :('
				pass
	
	if options.proxy in sys.argv: # Se separa la dir ip y el puerto
		for element in options.proxy.split(','):
			if '.' in element:
				try:
					socket.inet_aton(element)
					pvalues.append(element)
				except:
					print 'It could be a wrong IP address, please check it.'
					sys.exit(2)
				
			else:
				if int(element) > 65535:
					print "Por number not valid"
					sys.exit(2)
				else:
					pvalues.append(element)
			
			
	else:
		pvalues.append('')
		pvalues.append('')

	if options.report in sys.argv:
		for element in options.report.split(','):
			rvalues.append(element)
	else:
		pass
		
	
	if options.ojs in sys.argv: # Se manda a llamar la funcion del archivo
		ojs(options.ojs,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,tho)
		
		
	if options.moodle in sys.argv: # Se manda a llamar la funcion del archivo
		moodle(options.moodle,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thm)
		
			
	if options.crawlerHead in sys.argv and options.ojs in sys.argv: # Se manda a llamar la funcion del archivo
		crawlerHead(options.ojs,options.crawlerHead,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thc)
		
	elif options.crawlerHead in sys.argv and options.moodle in sys.argv:
		crawlerHead(options.moodle,options.crawlerHead,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thc)
		
	if options.Bruteforce in sys.argv and options.moodle in sys.argv: # Se manda a llamar la funcion del archivo
		for element in options.Bruteforce.split(','):
			bforce.append(element)
		url = options.moodle + bforce[0]
		check(url,bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thB)
		
		
	elif options.Bruteforce in sys.argv and options.ojs in sys.argv:
		for element in options.Bruteforce.split(','):
			bforce.append(element)
		url = options.ojs + bforce[0]
		check(url,bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thB)
		
			
	if options.bruteFile in sys.argv: # Se manda a llamar la funcion del archivo
		if options.moodle:
			url = options.moodle
		elif options.ojs:
			url = options.ojs
		for element in options.bruteFile.split(','):
			bforce.append(element)	
		checkFile(bforce[0],bforce[1],bforce[2],bforce[3],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,url,thb)
		

	if options.Crawler == True and options.moodle in sys.argv: # Se manda a llamar la funcion del archivo
		crawler(options.moodle,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thC)
		
	elif options.Crawler == True and options.ojs in sys.argv:
		crawler(options.ojs,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,thC)
		
	
	

getParams(arg)
