#!/usr/bin/python

import requests
import re
import sys
import argparse
import os

arg = ''
f = ''
url = ''

def crawlerHead(url,f):
	
	resources = []
	sites = []
	
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
		res = requests.head(other, allow_redirects=False)
		
		
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
					if element not in sites:
						sites.append(element)
						print 'Posible sitio: ' + element
			except:
				continue
		
			
			
	
	
		
		
		

def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Crawler usando metodo HEAD',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	
	parser.add_argument('-u', '--url', help='Site URL', required=True)				
	parser.add_argument('-f', '--file', help='File with resources', required=True)
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.url is not None and options.file is not None:
		crawlerHead(options.url,options.file)
	
	
		
getParams(arg)






