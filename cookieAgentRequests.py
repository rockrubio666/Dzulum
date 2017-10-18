#!/usr/bin/python

import requests
import argparse
import sys

arg = ''
cookie = ''
agent = ''
url = ''

def CookieAgent(url,cookie, agent):
	
	if len(agent) < 100:
		headers = {'user-agent': agent}
	else:
		print 'User-Agent no valido'
		sys.exit(2)
		
	if len(cookie) < 100:
		cookies = dict(cookies_are=cookie) 
		
	else:
		print 'Cookie no valida'
		sys.exit(2)

	r = requests.post(url, cookies=cookies, headers =  headers)
	print r.status_code
	

def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Prueba de Cookie y User-Agent',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	
	parser.add_argument('-c', '--cookie', help='Set Cookie')
	parser.add_argument('-a', '--agent', help='Set User-Agent')
	parser.add_argument('-u', '--url', help='Site URL', required=True)				
	
	options = parser.parse_args()
	
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.cookie is not None and options.agent is not None:
		CookieAgent(options.url,options.cookie,options.agent)
	elif options.cookie is None:
		CookieAgent(options.url,'',options.agent)
	elif options.agent is None:
		CookieAgent(options.url,options.cookie,'')	
	
		
getParams(arg)






