import hashlib # Utilizado para obtener los hashes
import re # Utilizado para las regex
import sys 
import csv #Utilizado para leer los archivos
import requests # Utilizado para realizar las peticiones
from lxml import etree #Utilizado para obtener los enlaces y archivos del sitio
from lxml import html # Utilizado para obtener los enlaces y archivos del sitio
import wget # Descarga los archivos necesarios
import os
from collections import Counter # Obtiene el promedio de las versiones
import operator
import time
from termcolor import colored
import socks # Tor
import socket # Tor


def ojs(arg,verbose,cookie,agent,proxip,proxport,tor,report):
	proxy = proxip  + ':' + proxport	
	proxies = {'http' : proxy, 'https' : proxy,}
	
	l = []
	
	requests.packages.urllib3.disable_warnings()
	
	
	if len(proxy) == 1:
		if tor == True: # USo de tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				req = requests.get(arg,verify=False)
			except:
				print 'It seems that we have problems using Tor :(, you could try with proxy option instead of'
				sys.exit(2)
		else:
			req = requests.get(arg,verify=False)
	else: # Uso de proxy	
		try:
			req = requests.post(arg,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print 'There\'s a problem with the proxy connection, please check it and try again :D '
			sys.exit(2)
		
	if cookie is None: # Obtiene la cookie de sesion
		for key,value in req.headers.iteritems():
			if 'set-cookie' in key:
				regex = re.compile(r'(OJSSID=)((.*);)')
				match = regex.search(value)
				try:
					if match.group():
						cookie = re.sub(r';(.*)','',match.group(2))
				except:
					print 'nio'
	else:
		pass
		
	if agent is None:
		agent = 'Kakeando'
	else:
		pass

	headers = {'user-agent': agent}
	cookies = {'': cookie}
	
	
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			req = requests.get(arg,cookies = cookies, headers = headers,verify=False)
		else:
			req = requests.get(arg, cookies = cookies, headers = headers,verify=False)
	else:
		req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False)
		
	
	page_source =  req.text
	regex = re.compile(r'(.*)(name="generator") content="(.*)"(.*)') # Se busca la meta etiqueta que contiene la version
	match = regex.search(page_source)

	try:
		if match.group():		
			if 'Open Journal Systems' in match.group():
				pass
			else:
				print colored('The site: ','yellow') + colored(match.group(3),'blue') + colored(' It could not be an OJS','yellow')
				sys.exit(2)
			if int(verbose) == 1:
				print "Site Version: " + colored(match.group(3),'green')
				l.append("Site Version: " + match.group(3))
				
			elif int(verbose) == 2:
				print "Site version: " + colored(arg, 'green') + " is: " + colored(match.group(3),'green')
				l.append("Site version: " + arg + " is: " + match.group(3))
			elif int(verbose) == 3:
				print "Site version: " + colored(arg, 'green') + " is: " + colored(match.group(3),'green')
				print "Site version found it in:" + colored(match.group(),'green')
				l.append("Site version: " + arg + " is: " + match.group(3) + 'Found it in: ' + match.group())
				
			
	except:
		version(arg,verbose,cookie,agent,proxy,proxies,tor,report,l) #Si no existe la meta etiqueta, busca en los archivos por defecto
	
	files(arg,verbose,match.group(3),cookie,agent,proxy,proxies,tor,report,l) # Si existe la version, busca los plugins
	
	
def version(arg,verbose,cookie,agent,proxy,proxies,tor,report,l): # Obtencion de la version mediante archivos
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href'] # Busca js, enlaces, imagenes y favicon
	
	requests.packages.urllib3.disable_warnings()					
	
	headers = {'user-agent': agent}
	cookies = {'': cookie}
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			req = requests.get(arg,cookies = cookies, headers = headers,verify=False)
		else:
			req = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False)
	
	webpage = html.fromstring(req.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)): # Busca los js, enlaces, imagenes y favicon del sitio
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				headers = {'user-agent': agent}
				cookies = dict(cookies_are=cookie) 
				if len(proxy) == 1:
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						#proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
						print  requests.get('http://httpbin.org/ip').content
						#req = requests.get(link,cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
						req = requests.get(link,cookies = cookies, headers = headers,verify=False)
					else:
						req = requests.get(link, cookies = cookies, headers = headers, verify=False)
				else:
					req = requests.get(link,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				
				if req.status_code == 200 and i in range(2,3): # Si es una imagen o favicon, se descarga y obtiene el hash
					try:
						filename = wget.download(link, bar=None)
						m.update(filename)
						hs = m.hexdigest()
						elements.append(hs)
						os.remove(filename)
					except:
						continue
				
				else: #Si es un js, se obtiene el hash
					try:
						m.update(req.text)
						hs =  m.hexdigest()
						elements.append(hs)
					except:
						continue
					
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')
			
	for element in elements: # Se realiza la comparacion con los valores que se tienen de sitios por defecto
		for row in reader:
			try:
				if element in row[2] and 'Ojs' in row[0]:
					print element
					average.append(row[1])
			except:
				continue
	f.close()

	cnt = Counter(average) # Se realiza el promedio para determinar la version
	if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
		v = max(cnt.iteritems(),key=operator.itemgetter(1))[0]
		print '\nVersion getting from configuration files: ' + colored(v, 'green')
		l.append('\nVersion getting from configuration files: ' + v)
	files(arg,verbose,v,cookie,agent,proxy,proxies,tor,report,l)
	
	
def files(arg,verbose,version,cookie,agent,proxy,proxies,tor,report,l): #Obtencion de plugins y temas
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	listThemes = ['//script/@src', '//@href']
	tmp = []
	requests.packages.urllib3.disable_warnings()					
	
	for row in reader:
		try:
			if 'Plugin' in row[1] and 'Ojs' in row[0]: # Se buscan plugins por defecto de los gestores de contenido
				plugin = arg + '/plugins' + row[2]
				
				headers = {'user-agent': agent}
				cookies = {'': cookie}
				if len(proxy) == 1:
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						req = requests.get(plugin,cookies = cookies, headers = headers,verify=False)
					else:
						req = requests.get(plugin, cookies = cookies, headers = headers, verify=False)
				else:
					req = requests.get(plugin,cookies = cookies, headers = headers,proxies = proxies,verify=False)
					
				if req.status_code == 200: # Si existe el archivo, obtiene el nombre del plugin y la version
					plugName = re.compile(r'=== (.*)')
					pN = plugName.search(req.text)
					plugVers = re.compile(r'(===) (Version(.*))')
					pV = plugVers.search(req.text)
					try:
						if pN.group():	
							try:
								if pV.group():
									if int(verbose) == 1:
										print "Plugin Name: " + colored(pN.group(1),'green')
										l.append("Plugin Name: " + pN.group(1))
										
									elif int(verbose) == 2:
										print "Plugin, Name: " + colored(pN.group(1),'green') + ' ,Path: ' + colored(plugin, 'green')
										l.append("Plugin, Name: " + pN.group(1) + ' ,Path: ' + plugin)
									elif int(verbose) == 3:
										print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green') + " " + colored(pV.group(2), 'blue')
										l.append("Plugin, Name: " + pN.group(1) + ' ,Path: ' + plugin + " " + pV.group(2))
							except:
								if int(verbose) == 1:
									print "Plugin Name: " + colored(pN.group(1), 'green') 
									l.append("Plugin Name: " + pN.group(1))
								elif int(verbose) == 2 or int(verbose) == 3:
									print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green')		
									l.append("Plugin, Name: " + pN.group(1) + ' ,Path: ' + plugin)
					except:
						continue
					
					regex = re.compile(r'(.*)\/(.*)\/README(.*)') # Archivos de configuracion visibles
					match = regex.search(plugin)
					try:
						if match.group():
							if int(verbose) == 1:
								print "Plugin Name: " + colored(match.group(2),'green')
								l.append("Plugin Name: " + match.group(2))
							elif int(verbose) == 2 or int(verbose) == 3:
								print "Plugin, Name: " + colored(match.group(2), 'green') + ' ,Path: ' + colored(plugin, 'green')
								l.append( "Plugin, Name: " + match.group(2) + ' ,Path: ' + plugin)
					except:
						continue
				
				else:
					continue
			
			if int(verbose) == 3:
				if 'Readme' in row[1] and 'Ojs' in row[0]:
					readme = arg + '/docs/release-notes/README-' + row[2]
				
					headers = {'user-agent': agent}
					cookies = {'': cookie}
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							req = requests.get(readme,cookies = cookies, headers = headers,verify=False)
						else:
							req = requests.get(readme, cookies = cookies, headers = headers, verify=False)
					else:
						req = requests.get(readme,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				
					if req.status_code == 200:
						print 'README file: ' + colored(readme, 'green')
						l.append('README file: ' + readme)
					else:
						continue
					
			
				elif 'Change' in row[1] and 'Ojs' in row[0]:	# Archivos de configuracion visibles
					changeLog = arg + '/docs/release-notes/ChangeLog-' + row[2]
				
					headers = {'user-agent': agent}
					cookies = {'': cookie}
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							req = requests.get(changeLog,cookies = cookies, headers = headers,verify=False)
						else:
							req = requests.get(changeLog, cookies = cookies, headers = headers, verify=False)
					else:
						req = requests.get(changeLog,cookies = cookies, headers = headers,proxies = proxies,verify=False)
	
					if req.status_code == 200:
						print 'ChangeLog: ' + colored(changeLog,'green')
						l.append('ChangeLog: ' + changeLog)
					else:
						continue
	
				elif 'Robots' in row[1] and 'Ojs' in row[0]: # Archivos de configuracion visibles
				
					headers = {'user-agent': agent}
					cookies = {'': cookie}
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							req = requests.get(arg + row[2],cookies = cookies, headers = headers,verify=False)
						else:
							req = requests.get(arg + row[2], cookies = cookies, headers = headers, verify=False)
					else:
						req = requests.get(arg + row[2],cookies = cookies, headers = headers,proxies = proxies,verify=False)
	
					if req.status_code == 200:
						print 'Robots file: ' + colored(req.url, 'green')
						l.append('Robots file: ' + req.url)
					else:
						continue
			else:
				continue
		except:
			continue
	f.close()
	
	headers = {'user-agent': agent}
	cookies = {'': cookie} 
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			req = requests.get(arg,cookies = cookies, headers = headers,verify=False)
		else:
			req = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False)
	
	webpage = html.fromstring(req.content)
	for i in range(0,len(listThemes)): # Busqueda de los temas instalados en el sitio
		for link in webpage.xpath(listThemes[i]):
			if 'theme' in link or 'journals' in link or 'themes' in link:
				tmp.append(link)
			else:
				continue
				
	for element in range(0,len(tmp)):
		if 'default' in tmp[element]: # Tema por defecto
			if int(verbose) == 1:
				print colored('Default Theme', 'green')
				l.append('Default Theme')
			elif int(verbose) == 2 or int(verbose) == 3:
				print colored( 'Default Theme', 'green') + ' Path: ' + colored(tmp[element], 'green')
				l.append('Default Theme' + ' Path: ' + tmp[element])
			element + i
		elif 'journals' in tmp[element]: #Tema journal
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():
					if int(verbose) == 1:
						print colored('Customize Theme ', 'green')
						l.append('Customize Theme ')
					elif int(verbose) == 2:
						print colored('Customize Theme, Name: ' + match.group(2), 'green')
						l.append('Customize Theme, Name: ' + match.group(2))
					elif int(verbose) == 3:	
						print 'Customize Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
						l.append('Customize Theme, Name: ' + match.group(2) + ', Path: ' + tmp[element])
					element + 1
			except:
				pass
		elif 'theme' in tmp[element]: 
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():
					if int(verbose) == 1:
						print 'Theme, Name: ' + colored(match.group(2),'green')
						l.append('Theme, Name: ' + match.group(2))
					elif int(verbose) == 2 or int(verbose) == 3:	
						print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
						l.append( 'Theme, Name: ' + match.group(2) + ', Path: ' + tmp[element])
			except:
				pass	
		elif 'bootstrap' in tmp[element]: # Tema creado con bootstrap
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():	
					if int(verbose) == 1:
						print 'Theme, Name: ' + colored(match.group(2),'green')
						l.append('Theme, Name: ' + match.group(2))
					elif int(verbose) == 2 or int(verbose) == 3:
						print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
						l.append('Theme, Name: ' + match.group(2) + ', Path: ' + tmp[element])
			except:
				pass	
		else:
			sys.exit
	vuln(version,verbose,report,l)

def vuln(version,verbose,report,l): # A partir de la version, se listan las posibles vulnerabilidades
	f = open('vuln','rb')
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		if 'Ojs' in row[0] and row[1] in version:
			if int(verbose) == 1:
				print "Vulnerability Link: " + colored(row[3],'green')
				l.append( "Vulnerability Link: " + row[3])
			elif int(verbose) == 2 or int(verbose) == 3:
				print "Vulnerability Name: " + colored(row[2],'green') + ' ,Vulnerability Link: ' + colored(row[3],'green')
				l.append( "Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + row[3])
	f.close()
	rep(report,l)
	

def rep(list1,list2):
	for value in list1:
		if list1.index(value) == 0:
			t = time.strftime('%d-%m-%Y')
			h = time.strftime('%H:%M:%S')
			fo = open(('OJSReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write('Results from the site\n')
			for element in list2:
				fo.write(element + '\n')
			fo.close()
		else:
			pass

	
	
	


