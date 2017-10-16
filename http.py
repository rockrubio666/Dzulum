#!/usr/bin/python


import argparse
import sys
import re
import socket
import urllib2
import ssl

arg = ''
url = ''
port = ''
site = ''

def http(url,port,site):
	
	if 'http://' not in url or 'https://' not in url: #Valida que tenga http
		try: #Valida tipo de dato
			var = int(port)
		except ValueError:
			print 'Puerto no valido'
			sys.exit(2)
		
		if int(port) > 0 and  int(port) <= 65535: 
			
				try: #Valida ip
					socket.inet_aton(url)
				except:
					print "ip no valida"
					sys.exit(2)	
					
				if 'http://' in site:
					proxy = "http://" + url + ":" + port
					proxy_support = urllib2.ProxyHandler({'http': proxy})
					opener = urllib2.build_opener(proxy_support)
					urllib2.install_opener(opener)
					html = urllib2.urlopen(site).read()
					print html
					
				elif 'https://' in site:
					ssl._create_default_https_context = ssl._create_unverified_context
					proxy = "https://" + url + ":" + port
					proxy_support = urllib2.ProxyHandler({'https': proxy})
					opener = urllib2.build_opener(proxy_support)
					urllib2.install_opener(opener)
					html = urllib2.urlopen(site).read()
					print html
					
					
				
		else:
			print "Puerto no valido"
			sys.exit(2)
		
def getParams(arg):
	parser = argparse.ArgumentParser(description='Proxy HTTP',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-p', '--proxy',
	nargs=3,metavar=('ip','port', 'sitio a consultar') ,help='')
					
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	elif '-p' in sys.argv or '--proxy':
		http(options.proxy[0],options.proxy[1],options.proxy[2])
		
getParams(arg)




