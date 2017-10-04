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
from bruteforce import *
from brutehttp import *
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
arg = ''  
		
def getParams(arg):
	bforce = []	
	pvalues = []
	rvalues = []
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
	description=( 						# Descripcion de las opciones de la herramienta
	'''				Vulnerability scanner for Moodle and OJS
-----------------------------------------------------------------------------------------------
 * Agent: Lets to specify the User Agent use it in the requests, e.g.: -a 'Thunderstruck'
 
 * Bruteforce: Tries to obtain the credentials of the site, parameters could be files, e.g.: /login/index.php,username,password,Users,Passwords,'Invalid Login'
	
 * Bruteforce with file: Tries to obtain the credentials of the site, this option needs a file with request, e.g.: my_request,Users,Passwords,'Invalid Login'
	
 * Cookie: Lets to specify the Session Cookie use it in the requests, e.g.: -k 'My_Cookie','Cuki'
 
 * Crawler with head requests: Look for possible links and javascript in the index page with help of a file, e.g.: -c sitesFile
 
 * Moodle: Searches elements necessaries to get the version and determine the possible vulnerabilities, e.g.: -m https://example.com/moodle/
 
 * Proxy: Sends requests through proxy, e.g.: -p 169.69.69.69,6969
 
 * OJS: Searches elements necessaries to get the version an determine the possible vulnerabilities, e.g.: -o https://example.com/ojs/
 
 * Report: Generates reports in TXT,HTML and XML from the results. They also could be sent via mail, e.g.: -r text,html,xml (The mail option will be asked when the program begins)
 
 * Tor: Makes requests through Tor socks, e.g.: -T
 
 * Verbose: Shows differents depuration levels, from 1 to 3, e.g.: -v 3	'''),
	epilog = 'Enjoy it! ')

# Opciones de la herramienta
	parser.add_argument('-a', '--Agent',metavar='Set User Agent', help='User Agent value')
	parser.add_argument('-B', '--Bruteforce',metavar='Login,UserField,PassField,User,Password,Message',help='Login = Url Login, User= Value or file, Password= Value o file, Message= Error Message')
	parser.add_argument('-b', '--bruteFile',metavar='RequestFile,User,Password,Message',help=' , User= Value or file, Password= Value o file, Message= Error Message')
	parser.add_argument('-c', '--crawlerHead', metavar='File', help = 'File with directories')	
	parser.add_argument('-k', '--Cookie',metavar='ID Cookie, Cookie Value', help='Cookide ID,Cookie value')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'URL from Moodle site')
	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'URL from OJS site')
	parser.add_argument('-p','--proxy',metavar='Proxy IP,Port', help = 'Proxy')
	parser.add_argument('-r','--report', metavar='Text,HTML,XML', help= 'Reports the results getting from the site')
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
	
	if options.Bruteforce in sys.argv and options.bruteFile in sys.argv: # Validacion para solo usar un bruteforce
		print parser.print_help()
		print '\n *** You can only execute one Bruteforce a time :,v ***'
		sys.exit(2)
	
	if options.proxy in sys.argv and options.tor == True: # Validacion para solo usar proxy o tor
		print parser.print_help()
		print '\n You can only use one proxy a time :,v ***'
		sys.exit(2)	
		
	if len(sys.argv) >= 3:
			numMeme = random.randint(0,5) #Generacion de banners
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

	if options.report in sys.argv: #Envio de los reportes por correo
		mail = raw_input('Do you want to send reports to your mail?[Y/n]') or 'Y'
		if 'Y' in mail or 'y' in mail:
			to = raw_input("Introduce your email: ")
		else:
			to = ''

		for element in options.report.split(','):
			rvalues.append(element)
	else:
		to = ''
		pass
		
			
	if options.crawlerHead in sys.argv and options.ojs in sys.argv: # Se manda a llamar la funcion del archivo
		crawlerHead(options.ojs,options.crawlerHead,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
	elif options.crawlerHead in sys.argv and options.moodle in sys.argv:
		crawlerHead(options.moodle,options.crawlerHead,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
	if options.Bruteforce in sys.argv and options.moodle in sys.argv: # Se manda a llamar la funcion del archivo
		for element in options.Bruteforce.split(','):
			bforce.append(element)
		url = options.moodle + bforce[0]
		check(url,bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
		
	elif options.Bruteforce in sys.argv and options.ojs in sys.argv: #Funcion de fuerza bruta
		for element in options.Bruteforce.split(','):
			bforce.append(element)
		url = options.ojs + bforce[0]
		check(url,bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
			
	if options.bruteFile in sys.argv: # Se manda a llamar la funcion del archivo
		if options.moodle:
			url = options.moodle
		elif options.ojs:
			url = options.ojs
		for element in options.bruteFile.split(','):
			bforce.append(element)	
		checkFile(bforce[0],bforce[1],bforce[2],bforce[3],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues,url)
		

	if options.ojs in sys.argv: # Se manda a llamar la funcion del archivo
		ojs(options.ojs,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
		
	if options.moodle in sys.argv: # Se manda a llamar la funcion del archivo
		moodle(options.moodle,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
	if len(to) == 0: #Envio de correos
		pass
	else:
		fromaddr = ""
		toaddr = to
		msg = MIMEMultipart()

		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "Reports"

		ind = ['BruteForce','CrawlerReport','OJSReport','MoodleReport']
		ext = ['.txt','.xml','.html']
		f = []
		dirs = os.listdir(os.getcwd())

		for element in dirs:
			for i in ind:
				if element.startswith(i):
					for e in ext:
						if element.endswith(e):
							f.append(element)
						else:
							pass
			
		for element in f:
			filename = str(element)
			attachment = open(os.getcwd() + '/' + element,'rb')
			part = MIMEBase('application','octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition',"attachment;filename=%s" % filename)
			msg.attach(part)

		try:
			server = smtplib.SMTP('smtp.gmail.com',587)
			server.starttls()
			server.login(fromaddr,'')
			text = msg.as_string()
			server.sendmail(fromaddr,toaddr,text)
			server.quit()
			print 'Mail sent successful!'
		except:	
			print 'Something went wrong, please check your mail and try again'
			sys.exit(2)


getParams(arg)
