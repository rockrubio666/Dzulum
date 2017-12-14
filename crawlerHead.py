#!/usr/bin/python

import requests # Utilizado para hacer las peticiones
import re # Utilizado para regex
import sys
import os
import time
from lxml.html import fromstring # Utilizado para exztraer los enlaces
from termcolor import colored
import socket # Tor
import socks # Tor

	

def crawlerHead(url,f,verbose,cookie,agent, proxip,proxport,tor,report):
	l = []
	requests.packages.urllib3.disable_warnings()
	if len(proxip) == 0:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050) # Peticiones a traves de tor
			socket.socket = socks.socksocket
			proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
			req = requests.get(url,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
		else:
			req = requests.get(url,verify=False)
	else: # Peticiones a traves del proxy
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		req = requests.get(url,proxies = {'http':proxy},verify=False)
	
	if cookie is None: # Obtencion de la cookie de sesion
		for key,value in req.headers.iteritems():
			if 'set-cookie' in key:
				regex = re.compile(r'(OJSSID=)((.*);)')
				match = regex.search(value)
				try:
					if match.group():
						cookie = re.sub(r';(.*)','',match.group(2))
				except:
						regex = re.compile(r'((.*)=)((.*);)')
						match = regex.search(value)
						try:
							if match.group():
								cookie = re.sub(r';(.*)','',match.group(3))
						except:
							print 'nio'
	
	else:
		pass
		
	if agent is None:
		agent = 'Kakeando'
	else:
		pass
		
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
			print "File not found"
	
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
			print "File not found"

	requests.packages.urllib3.disable_warnings() # Se revisa el location que devuelve con el recurso que no exite
	headers = {'user-agent': agent}
	cookies = {'': cookie} 
	if len(proxip) == 0:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
			req = requests.head(resources[0],cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
		else:
			req = requests.head(resources[0], cookies = cookies, headers = headers, verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		req = requests.head(resources[0],cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
			
	
	fake.append(req.url)
	for key,value in req.headers.iteritems():
		if 'location' in key:
			f = value
	
	
	resources.pop(0)
	print 'Looking for resources in: ' + colored(sites[0],'green')
	

	for element in resources: # Por cada elemento de la lista, se hace la peticion y se ve el codigo de estado
		
		other  = element.rstrip()
		requests.packages.urllib3.disable_warnings()					
		
		headers = {'user-agent': agent}
		cookies = {'': cookie} 
		if len(proxip) == 0:
			if tor == True:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
				socket.socket = socks.socksocket
				proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
				res = requests.get(other,cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
			else:
				res = requests.head(other, cookies = cookies, headers = headers, verify=False)
			res.connection.close()
		else:
			proxy = proxip  + ':' + proxport
			proxies = {'http' : proxy, 'https' : proxy,}
			res = requests.head(other,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
			res.connection.close()
		
		regex = re.compile(r'20[0-6]')
		match = regex.search(str(res.status_code))
		try:
			if match.group():	# Si el codigo de estado es 200, se muestra el recurso
				if element not in sites:
					sites.append(element)
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print "Resource exists: " + colored(element, 'green') + " Status code: " + colored(res.status_code, 'yellow')
						l.append("Resource exists: " + element + " Status code: " + str(res.status_code))
						
						
						
				else:
					continue
		except:
			reg = re.compile(r'30[0-7]') # Sie l codigo de estado es 300
			m3 = reg.search(str(res.status_code))
			try:
				if m3.group():
					if len(fake) == 20: # Y la lista de enlaces redirigidos es = 20, se detiene la ejecucion
						print 'Execution stopped for those links: '
						for element in fake:
							print colored(element, 'cyan')
						break
					else:
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							indexOf = res.url + '/'
							headers = {'user-agent': agent}
							cookies = {'': cookie} 
							if len(proxip) == 0:
								if tor == True:
									socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)	
									socket.socket = socks.socksocket
									proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
									r = requests.get(indexOf,cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
								else:
									r = requests.get(indexOf,cookies=cookies,headers=headers,verify=False)
							else:
								proxy = proxip  + ':' + proxport
								proxies = {'http' : proxy, 'https' : proxy,}
								r = requests.get(indexOf,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
								
							if r.status_code == 200 and '<title>Index of' in r.content: # Siel codigo de estado es 300, se verifica si muestra index of
								print "Index of: " + colored(r.url, 'green') + " Status code: " + colored(r.status_code, 'yellow')
								l.append("Index of: " + str(r.url) + " Status code: " + str(r.status_code))
							elif r.status_code == 200:
								print "Resource exists: " + colored(r.url, 'green') + " Status code: " + colored(r.status_code, 'yellow') # O si el codigo de estado es 200
								l.append( "Resource exists: " + str(r.url) + " Status code: " + str(r.status_code))
							elif r.status_code == 403: # Si es un forbidden, se vuelve a pasar la lista de sitios
								if os.path.exists(f):
									fo = open(f, 'r')
									for line in fo:
										new = r.url + line
										headers = {'user-agent': agent}
										cookies = {'': cookie} 
										if len(proxip) == 0:
											if tor == True:
												socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
												socket.socket = socks.socksocket
												proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
												rn = requests.head(new.rstrip('\n'),cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
											else:
												rn = requests.head(new.rstrip('\n'),cookies=cookies,headers=headers,verify=False)
										else:
											proxy = proxip  + ':' + proxport
											proxies = {'http' : proxy, 'https' : proxy,}
											rn = requests.head(new.strip('\n'),cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
			
		
										if rn.status_code == 200:
											print "Resource exists: " + colored(rn.url, 'green') + " Status code: " + colored(rn.status_code, 'yellow')
											l.append("Resource exists: " + str(rn.url) + " Status code: " + str(rn.status_code))
									fo.close()
								else:
									print "File not found"
								
						for key, value in res.headers.iteritems():
							if 'location' in key: 
								if value in f:
									fake.append(res.url)	
						
			except:
				pass
	
	rep(report,l)
	
def rep(list1,list2):
	for value in list1:
		if list1.index(value) == 0:
			t = time.strftime('%d-%m-%Y')
			h = time.strftime('%H:%M:%S')
			fo = open(('CrawlerReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write('Results from the site\n')
			for element in list2:
				fo.write(element + '\n')
			fo.close()
		else:
			pass
