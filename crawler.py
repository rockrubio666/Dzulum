#!/usr/bin/python
import re
import requests
import sys
import argparse
from lxml import etree
from lxml import html
from termcolor import colored
import socket
import socks

visited = []
toVisit = []


def crawler(arg,verbose,cookie,agent,proxip,proxport,tor):
	
	requests.packages.urllib3.disable_warnings()
	if len(proxip) == 0:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
			req = requests.get(arg,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
		else:
			req = requests.get(arg,verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		req = requests.get(arg,proxies = {'http':proxy},verify=False)
		
	if cookie is None:
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
	
	print colored("Beginning Crawling", 'blue')
	print 'Consulta del sitio: ' + colored(arg, 'green')
	if 'http://' in arg or 'https://' in arg: # Valida si tiene http(s)
		# Lista para encontrar elementos
		listFind = [ '//a/@href',  '//script/@src']
		
		# Peticiones
		try:
			requests.packages.urllib3.disable_warnings()					
			
			headers = {'user-agent': agent}
			cookies = {'': cookie} 
			if len(proxip) == 0:
				if tor == True:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket
					proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
					res = requests.get(arg,cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
				else:
					res = requests.get(arg, cookies = cookies, headers = headers, verify=False)
			else:
				proxy = proxip  + ':' + proxport
				proxies = {'http' : proxy, 'https' : proxy,}
				req = requests.get(arg,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
			
			page_source = res.text
			webpage = html.fromstring(res.content)
			
		except:
			print "Error, no se pudo consultar el sitio"
			sys.exit(2)
			
		
		# Extrae los elementos de la pagina principal
		i = 0
		site =  re.sub(r'(http|https)://','',arg)
		
		for i in range(0,len(listFind)):
			for link in webpage.xpath(listFind[i]):
				if site in link: # Para los enlaces que contienen el nombre de dominio
					regex = re.compile(r'(.*)\.js') #Si el enlace contiene js se agrega a una lista que no se consulta
					js = regex.search(link)
					try:
						if js.group() not in visited:
							if int(verbose) == 2 or int(verbose) == 3:
								print 'Link: ' + colored(js.group(),'blue')
							visited.append(link)
					except:
						regex = re.compile(r'(.*)\?(.*)') # Quita las variables despues de ?
						match = regex.search(link)
						try:
							if match.group():
								if match.group(1) not in toVisit and match.group(1) not in visited:
									print 'Link: ' + colored(match.group(1),'blue')
									toVisit.append(match.group(1))
						except:
							if link not in toVisit and link not in visited: #Si el enlace no tiene variables
								print 'Link: ' + colored(link,'blue')
								toVisit.append(link)
					
				else: #Otros enlaces Ej:'/'
					regex = re.compile(r'^\/(.*)') # Agrega los que tienen solo diagonal
					diagonal = regex.search(link)
					try:
						if diagonal.group():
							complete =  arg + link
							headers = {'user-agent': agent}
							cookies = {'': cookie} 
							if len(proxip) == 0:
								r = requests.head(complete, cookies = cookies, headers = headers, verify=False)
							else:
								proxy = proxip  + ':' + proxport
								proxies = {'http' : proxy, 'https' : proxy,}
								r = requests.head(complete,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
							
							
							regex = re.compile(r'20[0-6]')
							status = regex.search(str(r.status_code))
							try:
								if status.group():
									if complete not in toVisit and complete not in visited:
										print 'Link: ' + colored(complete,'blue')
										toVisit.append(complete)
							except:
								continue
					except:
						continue
			
			i + 1	
		
		
	else: # Si no tiene http
			http =  re.sub(r'(^)','http://',arg)
			crawler(http)
			exit(2)
	
	#for element in range(len(toVisit)):
	#	visited.append(toVisit[element])
	#	print colored(toVisit[element], 'blue')
		#toVisit.pop(element)
		
		#crawler(toVisit[element])
	
	

