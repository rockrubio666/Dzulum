#!/usr/bin/python

import requests
import re
import sys
import os
from termcolor import colored

	

def crawlerHead(url,f,verbose,cookie,agent, proxip,proxport):
	print colored('\nBeginning Crawling with Head request', 'green')
	fake = []
	conLen = []
	resources = []
	sites = []
	proxy = proxip + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
		
	if url.endswith('/'): # Si la URL termina con /, se agrega la cadena para validar multiples redirecciones
		sites.append(url)
		resources.append(url + 'ashfiemvmqwfhejfqkfwoe')
		if os.path.exists(f):
			fo = open(f, 'r')
			for line in fo:
				union = url + line
				resources.append(union)	
			fo.close()
		else:
			print "No se encontro el archivo"
	
	else:
		sites.append(url + '/') # Si la URL no tiene /, se agrega la '/' y la cadena para validar multiples redirecciones
		resources.append(url + '/ashfiemvmqwfhejfqkfwoe')
		if os.path.exists(f):
			fo = open(f, 'r')
			for line in fo:
				union = url + '/' + line
				resources.append(union)	
			fo.close()
		else:
			print "No se encontro el archivo"

	requests.packages.urllib3.disable_warnings() # Se revisa el location que devuelve con el recurso que no exite
	if len(proxip) == 0:
		if cookie is None and agent is None:
			req = requests.head(resources[0], verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.post(resources[0],headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.post(resources[0], cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.post(resources[0], cookies = cookies, headers = headers, verify=False)
			
	else:
		if cookie is None and agent is None:
			req = requests.head(resources[0], proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.post(resources[0],headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.post(resources[0], cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.post(resources[0], cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
	
	
	fake.append(req.url)
	for key,value in req.headers.iteritems():
		if 'location' in key:
			f = value
	
	
	resources.pop(0)
	print 'Buscando recursos en: ' + colored(sites[0],'green')
	

	for element in resources: # Por cada elemento de la lista, se hace la peticion y se ve el codigo de estado
		other  = element.rstrip()
		requests.packages.urllib3.disable_warnings()					
		
		if len(proxip) == 0:
			if cookie is None and agent is None:
				res = requests.head(other, verify=False)
			
			elif cookie is None and agent is not None:
				headers = {'user-agent': agent}
				res = requests.head(other,headers = headers, verify=False)
		
			elif cookie is not None and agent is None:
				cookies = dict(cookies_are=cookie) 
				res= requests.head(other, cookies = cookies, verify=False)
		
			elif cookie is not None and agent is not None:
				headers = {'user-agent': agent}
				cookies = dict(cookies_are=cookie) 
				res = requests.head(other, cookies = cookies, headers = headers, verify=False)
		
		else:
			if cookie is None and agent is None:
				res = requests.head(other, proxies = {'http':proxy},verify=False)
			
			elif cookie is None and agent is not None:
				headers = {'user-agent': agent}
				res = requests.head(other,headers = headers, proxies = {'http':proxy},verify=False)
		
			elif cookie is not None and agent is None:
				cookies = dict(cookies_are=cookie) 
				res= requests.head(other, cookies = cookies, proxies = {'http':proxy},verify=False)
		
			elif cookie is not None and agent is not None:
				headers = {'user-agent': agent}
				cookies = dict(cookies_are=cookie) 
				res = requests.head(other, cookies = cookies, headers = headers,proxies = {'http':proxy}, verify=False)
	
		
		res.connection.close()
		
		regex = re.compile(r'20[0-6]')
		match = regex.search(str(res.status_code))
		try:
			if match.group():	# Si el codigo de estado es 200, se muestra el recurso
				if element not in sites:
					sites.append(element)
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print "Existe el recurso: " + colored(element, 'green')
				else:
					continue
		except:
			regex = re.compile(r'30[0-7]') # Si el codigo de estado es 300
			match = regex.search(str(res.status_code))
			try:
				if match.group():
					if len(fake) == 20:
						print 'Se detuvo la ejecucion por los siguientes enlaces: '
						for element in fake:
							print colored(element, 'cyan')
						break
					else:
						if int(verbose) == 2 or int(verbose) == 3:
							print colored('Posible recurso: ', 'yellow') + colored(element,'blue')				
						for key, value in res.headers.iteritems():
							if 'location' in key: 
								if value in f:
									fake.append(res.url)			
			except:
				continue
		
