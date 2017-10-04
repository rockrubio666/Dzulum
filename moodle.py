#!/usr/bin/python
import argparse
import socket
import re
import sys
import requests

arg = ''

def ojsMoodleOther(arg):
# Si el argumento tiene http(s)
	if 'http://' in arg or 'https://' in arg:
		res = requests.get(arg)
		page_source = res.text
		regex = re.compile(r'(.*)name="keywords" content="moodle(.*)')
		match = regex.search(page_source)
		try:
			if match.group():
				print "Es un moodle"
				#sys.exit(2)
		except:
			print "No es moodle"
			sys.exit(2)
		
# Si no tiene http(s) se pega a la direccion
	else:
		http =  re.sub(r'(^)','http://',arg)
		ojsMoodleOther(http)
		exit(2)
		
#############Considerar agregar https		



def validateUrl(arg):
#Aisla dominio y direccion ip
	
	if 'https://' in arg or 'http://' in arg:
		http  = re.sub('(http|https)://','',arg)
		validateUrl(http)
		
		
	else: # Si no tiene http(s), pero tiene directorios
		if '/' in arg:
			
			var = re.sub('/(.*)','',arg)
			validateUrl(var)	
			
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
						sys.exit(2)
		
					try:
						site = socket.gethostbyaddr(arg)
						print "Sitio: " + site[0]
					except:
						print "no se puede determinar el sitio"
						exit
					
			except: # Valida dominio
				
				try:
					site = socket.gethostbyname(arg)
					print "Ip: " + site
					print "Sitio: " + arg
				
				except:
					print "Sitio no valido"
					sys.exit(2)
					
	
	ojsMoodleOther(arg)

def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-u', '--url', help='Direccion URL del sitio')
					
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
		
	
	elif '-u' in sys.argv or '--url':
		validateUrl(options.url)
		
		
getParams(arg)





