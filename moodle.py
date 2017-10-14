#!/usr/bin/python
import getopt
import socket
import re
import sys

arg = ''

def validateUrl(arg):
#Aisla dominio y direccion ip

	if 'https' in arg or 'http' in arg:
		arg  = re.sub('(http|https)://','',arg)
		arg = re.sub('/(.*)','',arg)	
		validateUrl(arg)
		
	else:
		ip = re.compile(r'([0-9]{1,}\.){3}([0-9]{1,})') # Determina si es ip
		match = ip.search(arg)
		try:
			if match.group():
				try: #Valida ip
					socket.inet_aton(arg)
					print "Ip: " + arg
				except:
					print "ip no valida"
					return 0
		
				try:
					site = socket.gethostbyaddr(arg)
					print "Sitio: " + site[0]
				except:
					print "no se puede determinar el sitio"
					return 0
		
		except: # Valida dominio
			try:
			
				site = socket.gethostbyname(arg)
				print "Ip: " + site
				print "Sitio: " + arg
			except:
				print "Sitio no valido"
				return 0
			
def help():
	print('-u, --url URL del sitio a analizar \n'
		  '-h, ---help Ayuda\n')




def getParams(arg):
	try:
		opts, args = getopt.getopt(sys.argv[1:],'u:h', ['url=', 'help'])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:	
		if opt in ('-u','--url'):
			url = arg
			validateUrl(url)
	
		
		elif opt in ('-h','--help'):
			h = arg
			help()
					
		else:
			print 'opcion no valida'
			sys.exit(2)


getParams(arg)


'''
def ojsMoodleOther(arg):
	response = urllib2.urlopen(arg)
	page_source = response.read()
	regex = re.compile(r'(.*)name="keywords" content="moodle(.*)')
	match = regex.search(page_source)
	if match.group():
		print "Es un moodle"
	else:
		print "No es moodle"
'''
