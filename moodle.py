#!/usr/bin/python
import argparse
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
				print arg
				site = socket.gethostbyname(arg)
				print "Ip: " + site
				print "Sitio: " + arg
			except:
				print "Sitio no valido"
				return 0
			

def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-u', '--url', help='Direccion URL del sitio')
					
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
		print sys.argv
	
	elif '-u' in sys.argv or '--url':
		validateUrl(options.url)
		
		
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
