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
import random

def ojs(arg,verbose,cookie,agent,proxip,proxport,tor,report):
	
	if 'http' in arg:
		pass
		if 'index.php' in arg:
			ind = raw_input('If you don\'t introduce the principal page, you couldn\'t get enough evidence. Do yo want to continue? [y/N] ') or 'N'
			if 'Y' in ind or 'y' in ind:
				pass
			else:
				print colored('Check the URL and try again :D ', 'green')
				sys.exit(2)
	else:
		print colored('The URL doesn\'t have http or https, please check it and try again :D ','green')
		sys.exit(2)
	
	proxy = proxip  + ':' + proxport	
	proxies = {'http' : proxy, 'https' : proxy,}
	
	l = []
	
	requests.packages.urllib3.disable_warnings()
	
	if len(proxy) == 1:
		if tor == True: # USo de tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
			try:
				req = requests.get(arg,verify=False,timeout=10)
			except requests.RequestException:
				print colored(error,'green')
				sys.exit(2)
			
			except requests.exceptions.ConnectionError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)
		else: # Sin anonimato
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
			try:
				req = requests.get(arg,verify=False,timeout=10)			
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)
				
	else: # Uso de proxy	
		error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
		try:
			req = requests.post(arg,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)

	if cookie is None: # Obtiene la cookie de sesion
		for key,value in req.headers.iteritems():
			if key.startswith('set-cookie'):
				previous = value.split(';')[0].split('=')
				cookies = {previous[0] : previous[1]}
			else:
				pass
		
		if cookie is None:
			alp = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
			cook = []
			while len(cook) < 26:
				cook.append(random.choice(alp))
			c =  "".join(str(element) for element in cook)
			cookies = {'Random_Cookie' : c}
	
	else:
		jar = cookie.split(',')
		cookies = {jar[0]:jar[1]}
		
	if agent is None:
		agent = 'Mozilla/5.0 (PLAYSTATION 3;3.55)'
		headers = {'user-agent': agent}
	else:
		headers = {'user-agent': agent}

	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
			try:
				req = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)

		else:
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
			try:
				req = requests.get(arg, cookies = cookies, headers = headers,verify=False,timeout=10)			
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)

	else:
		error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
		try:
			req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
		
	
	
	page_source =  req.text
	if '/lib/pkp/js' in page_source:
		pass
	else:
		print colored('The site: ','yellow') +  colored(arg, 'blue') + colored(' isn\'t an OJS','yellow')
		sys.exit(2)
		
	regex = re.compile(r'(.*)(name="generator") content="(.*)"(.*)') # Se busca la meta etiqueta que contiene la version
	match = regex.search(page_source)

	try:
		if match.group():		
			r = requests.get('http://httpbin.org/ip')
			t = re.compile(r'"origin":(.*)')
			mat = t.search(r.content)
			if mat.group():
				print mat.group(1).replace("\"","")
			else:
				pass
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
		version(arg,verbose,cookies,headers,proxy,proxies,tor,report,l) #Si no existe la meta etiqueta, busca en los archivos por defecto
	files(arg,verbose,match.group(3),cookies,headers,proxy,proxies,tor,report,l) # Si existe la version, busca los plugins
	
	
def version(arg,verbose,cookies,headers,proxy,proxies,tor,report,l): # Obtencion de la version mediante archivos
	print colored('We\'re trying to get the version through default files, please wait','green')
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href'] # Busca js, enlaces, imagenes y favicon
	
	requests.packages.urllib3.disable_warnings()					
	
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
			try:
				req = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)
		else:
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
			try:
				req = requests.get(arg, cookies = cookies, headers = headers, verify=False,timeout=10)			
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)
	else:
		error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
		try:
			req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
	
	webpage = html.fromstring(req.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)): # Busca los js, enlaces, imagenes y favicon del sitio
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				if len(proxy) == 1:
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
						try:
							req = requests.get(link,cookies = cookies, headers = headers,verify=False,timeout=10)
						except requests.RequestException:						
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
					else:
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
						try:
							req = requests.get(link, cookies = cookies, headers = headers, verify=False,timeout=10)						
						except requests.RequestException:						
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
			
				else:
					error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
					try:
						req = requests.get(link,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)					
					except requests.RequestException:					
						print colored(error,'green')
						sys.exit(2)
					except:
						print colored(error,'green')
						sys.exit(2)
				
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
					average.append(row[1])
			except:
				continue
	f.close()

	cnt = Counter(average) # Se realiza el promedio para determinar la version
	if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
		try:
			v = max(cnt.iteritems(),key=operator.itemgetter(1))[0]
		except ValueError:
			print colored('Sorry, It couldn\'t get the version of the OJS, please try again later :(','green')
			sys.exit(2)
		print '\nVersion getting from configuration files: ' + colored(v, 'green')
		l.append('\nVersion getting from configuration files: ' + v)
		files(arg,verbose,v,cookies,headers,proxy,proxies,tor,report,l)
		
	
def files(arg,verbose,version,cookies,headers,proxy,proxies,tor,report,l): #Obtencion de plugins y temas
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	listThemes = ['//script/@src', '//@href']
	tmp = []
	requests.packages.urllib3.disable_warnings()					
	
	for row in reader:
		try:
			if 'Plugin' in row[1] and 'Ojs' in row[0]: # Se buscan plugins por defecto de los gestores de contenido
				plugin = arg + '/plugins' + row[2]
				
				if len(proxy) == 1:
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
						try:
							req = requests.get(plugin,cookies = cookies, headers = headers,verify=False,timeout=10)
						except requests.RequestException:		
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)

					else:
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
						try:
							req = requests.get(plugin, cookies = cookies, headers = headers, verify=False,timeout=10)						
						except requests.RequestException:						
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
			

				else:
					error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
					try:
						req = requests.get(plugin,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)					
					except requests.RequestException:					
						print colored(error,'green')
						sys.exit(2)
					except:
						print colored(error,'green')
						sys.exit(2)
					
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
				
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
							try:
								req = requests.get(readme,cookies = cookies, headers = headers,verify=False,timeout=10)
							except requests.RequestException:							
								print colored(error,'green')
								sys.exit(2)
							except:
								print colored(error,'green')
								sys.exit(2)

						else:
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
							try:
								req = requests.get(readme, cookies = cookies, headers = headers, verify=False,timeout=10)							
							except requests.RequestException:							
								print colored(error,'green')
								sys.exit(2)
							except:
								print colored(error,'green')
								sys.exit(2)

					else:
						try:
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
							req = requests.get(readme,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)						
						except requests.RequestException:						
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
				
					if req.status_code == 200:
						print 'README file: ' + colored(readme, 'green')
						l.append('README file: ' + readme)
					else:
						continue
					
			
				elif 'Change' in row[1] and 'Ojs' in row[0]:	# Archivos de configuracion visibles
					changeLog = arg + '/docs/release-notes/ChangeLog-' + row[2]
				
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
							try:
								req = requests.get(changeLog,cookies = cookies, headers = headers,verify=False,timeout=10)
							except requests.RequestException:							
								print colored(error,'green')
								sys.exit(2)
							except:
								print colored(error,'green')
								sys.exit(2)

						else:
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
							try:
								req = requests.get(changeLog, cookies = cookies, headers = headers, verify=False,timeout=10)							
							except requests.RequestException:							
								print colored(error,'green')
								sys.exit(2)
							except:
								print colored(error,'green')
								sys.exit(2)
			

					else:
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
						try:
							req = requests.get(changeLog,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)						
						except requests.RequestException:						
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
	
					if req.status_code == 200:
						print 'ChangeLog: ' + colored(changeLog,'green')
						l.append('ChangeLog: ' + changeLog)
					else:
						continue
	
				elif 'Robots' in row[1] and 'Ojs' in row[0]: # Archivos de configuracion visibles
				
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
							try:
								req = requests.get(arg + row[2],cookies = cookies, headers = headers,verify=False,timeout=10)
							except requests.RequestException:							
								print colored(error,'green')
								sys.exit(2)
							except:
								print colored(error,'green')
								sys.exit(2)

						else:
							error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
							try:
								req = requests.get(arg + row[2], cookies = cookies, headers = headers, verify=False,timeout=10)							
							except requests.RequestException:							
								print colored(error,'green')
								sys.exit(2)
							except:
								print colored(error,'green')
								sys.exit(2)
			

					else:
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
						try:
							req = requests.get(arg + row[2],cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)						
						except requests.RequestException:						
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
	
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
	
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in the URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
			try:
				req = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)
		else:
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
			try:
				req = requests.get(arg, cookies = cookies, headers = headers, verify=False,timeout=10)			
			except requests.RequestException:			
				print colored(error,'green')
				sys.exit(2)
			except:
				print colored(error,'green')
				sys.exit(2)
			

	else:
		error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
		try:
			req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
	
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
		try:
			if 'Ojs' in row[0] and row[1] in version:
				if int(verbose) == 1:
					print "Vulnerability Link: " + colored(row[3],'green')
					l.append( "Vulnerability Link: " + row[3])
				elif int(verbose) == 2 or int(verbose) == 3:
					print "Vulnerability Name: " + colored(row[2],'green') + ' ,Vulnerability Link: ' + colored(row[3],'green')
					l.append( "Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + row[3])
		except IndexError:
			pass
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
