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
from directoryBforce import *
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
-----------------------------------------------------------------------------------------------'''),
	epilog = 'Enjoy it! ')

# Opciones de la herramienta
	parser.add_argument('-a', '--Agent',metavar='Set User Agent', help='Lets to specify the User Agent use it in the requests, e.g.: -a \'Thunderstruck\'')
	parser.add_argument('-B', '--Bruteforce',metavar='Login,UserField,PassField,User,Password,Message',help='Tries to obtain the credentials of the site, parameters could be files, e.g.: /login/index.php,username,password,Users,Passwords,\'Invalid Login\'')
	parser.add_argument('-b', '--bruteFile',metavar='RequestFile,User,Password,Message',help='Tries to obtain the credentials of the site, this option needs a file with request, e.g.: my_request,Users,Passwords,\'Invalid Login\'')
	parser.add_argument('-d', '--directoryBforce', metavar='File', help = 'Look for possible links and javascript in the index page with help of a file, e.g.: -c sitesFile')	
	parser.add_argument('-k', '--Cookie',metavar='ID Cookie, Cookie Value', help='Lets to specify the Session Cookie use it in the requests, e.g.: -k \'My_Cookie\',\'Cuki\'')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'Searches elements necessaries to get the version and determine the possible vulnerabilities, e.g.: -m https://example.com/moodle/')
	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'Searches elements necessaries to get the version an determine the possible vulnerabilities, e.g.: -o https://example.com/ojs/')
	parser.add_argument('-p','--proxy',metavar='Proxy IP,Port', help = 'Sends requests through proxy, e.g.: -p 169.69.69.69,6969')
	parser.add_argument('-r','--report', metavar='Text,HTML,XML', help= 'Generates reports in TXT,HTML and XML from the results. They also could be sent via mail, e.g.: -r text,html,xml (The mail option will be asked when the program begins)')
	parser.add_argument('-T','--tor', help = 'Makes requests through Tor socks, e.g.: -T',action='store_true')
	parser.add_argument('-v','--verbose', metavar='Number', nargs = '?',help='Shows differents depuration levels, from 1 to 3, e.g.: -v 3', default = 1)
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
			fo = open('mail.conf','r')
			for line in fo:
				if '@' in line and len(line) > 100:
					pass
				else:
					test = line
					if '96h69k5JayTY@gmail.com:BvR%s4v28X#?' in line:
						print colored('Please modify the default values in mail.conf and try to send the reports again', 'yellow')
						sys.exit(2)
					else:
						t = test.split(':')
						mail = t[0]
						pas = t[1]
						to = raw_input("Introduce your email: ")
		else:
			to = ""	
			pass
		
		for element in options.report.split(','):
				rvalues.append(element)
	else:
		to = ''
			
			
	if options.directoryBforce in sys.argv and options.ojs in sys.argv: # Se manda a llamar la funcion del archivo
		directoryBforce(options.ojs,options.directoryBforce,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
	elif options.directoryBforce in sys.argv and options.moodle in sys.argv:
		directoryBforce(options.moodle,options.directoryBforce,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1],options.tor,rvalues)
		
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
		fromaddr = mail
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
			server.login(fromaddr, pas)
			text = msg.as_string()
			server.sendmail(fromaddr,toaddr,text)
			server.quit()
			print 'Mail sent successful!'
		except:	
			print 'Something went wrong, please check the configuration in mail.conf or the mail gave at the beginning of the execution and try again'
			sys.exit(2)


getParams(arg)
