#!/usr/bin/python

import requests
import re
import sys
import argparse
import os
from termcolor import colored
arg = ''
f = ''
url = ''

def crawlerHead(url,f):
	
	fake = []
	conLen = []
	resources = []
	sites = []
	
	
	resources.append(url + '/ashfiemvmqwfhejfqkfwoe')
		
	
	if os.path.exists(f):
		fo = open(f, 'r')
		for line in fo:
			union = url + '/' + line
			resources.append(union)	
		fo.close()
	else:
		print "No se encontro el archivo"

	sites.append(url)
	
	
	for element in resources:
		other  = element.rstrip()
		requests.packages.urllib3.disable_warnings()					
		res = requests.head(other, verify=False)
		res.connection.close()
		#res1 = requests.get(other)
		
		regex = re.compile(r'20[0-6]')
		match = regex.search(str(res.status_code))
		try:
			if match.group():	
				if element not in sites:
					sites.append(element)
					print colored("Existe el recurso: ",'white') + colored(element, 'green')
				else:
					continue
		except:
			continue
			regex = re.compile(r'30[0-7]')
			match = regex.search(str(res.status_code))
			try:
				if match.group():
					print colored('Posible recurso: ') + colored(element,'green')
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







