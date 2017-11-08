#!/usr/bin/python

import requests
import re
import sys
import argparse
import os

arg = ''
f = ''
url = ''
s = ''

def crawlerHead(url,f,s):
	
	fake = []
	conLen = []
	resources = []
	sites = []
	chain = s
	
	if len(chain) <= 15:
		print 'Error, string must be longer than 15 characters'
		sys.exit(2)
	else:
		union = url + '/' + chain
		resources.append(union)
		
			
	
	if os.path.exists(f):
		fo = open(f, 'r')
		for line in fo:
			union = url + line
			resources.append(union)	
		fo.close()
	else:
		print "No se encontro el archivo"

	sites.append(url)
	
	
	for element in resources:
		other  = element.rstrip()
		res = requests.head(other)
		res1 = requests.get(other)
		
		regex = re.compile(r'20[0-6]')
		match = regex.search(str(res.status_code))
		try:
			if match.group():	
				if element not in sites:
					sites.append(element)
					print "Existe el recurso: " + element
				else:
					continue
		except:
			regex = re.compile(r'30[0-7]')
			match = regex.search(str(res.status_code))
			try:
				if match.group():
					for key, value in (res.headers).iteritems(): # Verifica a donde se redirige
						if key.startswith('location') :
							var = other + '/'
							if str(other) not in value or str(var) not in value: # Si no es igual al directorio que se le paso
								for key, value in (res1.headers).iteritems(): # Se verifica el content-lenght del primer directorio
									if key.startswith('content-length') :
										if  len(conLen) == 0:
											conLen.append(value)
											fake.append(other)
						
										elif len(conLen) > 0 and len(conLen) <= 5:
											if (int(value) + 5) > int(conLen[0]) or (int(value) - 5) < int(conLen[0]):
												conLen.append(value)
												fake.append(other)
											
										elif len(conLen) > 5:
											print 'Se detuvo del programa debido a que los siguientes directorios no existen'
											for element in fake:
												print element
											sys.exit(2)	
									sys.exit(2)	
							
							
							else:				
								if element not in sites:
									sites.append(element)
									print "Existe el recurso: " + element
							
			except:
				continue
		
			
		
		

def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Crawler usando metodo HEAD',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	
	parser.add_argument('-u', '--url', help='Site URL', required=True)				
	parser.add_argument('-f', '--file', help='File with resources', required=True)
	parser.add_argument('-s', '--string', help='String to validate site', required=True)
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.url is not None and options.file is not None and options.string is not None:
		crawlerHead(options.url,options.file,options.string)
	
	
		
getParams(arg)







