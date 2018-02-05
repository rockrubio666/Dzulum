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
import time

start_time = time.time() #Tiempo de ejecucion del programa
def ojs(arg,verbose,cookie,agent,proxip,proxport,tor,report):
	print colored("\nBeginning OJS scanner",'yellow')
	if 'http' in arg:
		pass
		if 'index.php' in arg: #Validacion de la pagina principal del sitio
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
	
	ver = []
	
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
		
		if cookie is None: #cookie aleatoria
			alp = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
			cook = []
			while len(cook) < 26:
				cook.append(random.choice(alp))
			c =  "".join(str(element) for element in cook)
			cookies = {'Random_Cookie' : c}
	
	else:
		jar = cookie.split(',')
		cookies = {jar[0]:jar[1]}
		
	if agent is None: #User agent por defecto
		agent = 'Mozilla/5.0 (PLAYSTATION 3;3.55)'
		headers = {'user-agent': agent}
	else:
		headers = {'user-agent': agent}

	if len(proxy) == 1:
		if tor == True: #Manejo de errores de tor
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

		else: #Manejo de errores de la peticion
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

	else: #Manejo de errores del proxy
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
	if '/lib/pkp/js' in page_source: #Validacion de OJS
		pass
	else:
		print colored('The site: ','yellow') +  colored(arg, 'blue') + colored(' isn\'t an OJS','yellow')
		sys.exit(2)
		
	regex = re.compile(r'(.*)(name="generator") content="(.*)"(.*)') # Se busca la meta etiqueta que contiene la version
	match = regex.search(page_source)
	
	
		
	try:
		if match.group():		
			if int(verbose) == 1:
				print "Site Version: " + colored(match.group(3),'green')
				
				
			elif int(verbose) == 2:
				print "Site version: " + colored(arg, 'green') + " is: " + colored(match.group(3),'green')
				
			elif int(verbose) == 3:
				print "Site version: " + colored(arg, 'green') + " is: " + colored(match.group(3),'green')
				print "Site version found it in:" + colored(match.group(),'green')
			ver.append(match.group(3))
			ver.append(match.group())
				
				
	except:
		version(arg,verbose,cookies,headers,proxy,proxies,tor,report,ver) #Si no existe la meta etiqueta, busca en los archivos por defecto
	files(arg,verbose,match.group(3),cookies,headers,proxy,proxies,tor,report,ver) # Si existe la version, busca los plugins
	
	
def version(arg,verbose,cookies,headers,proxy,proxies,tor,report,ver): # Obtencion de la version mediante archivos
	print colored('We\'re trying to get the version through default files, please wait','green')
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href'] # Busca js, enlaces, imagenes y favicon
	
	requests.packages.urllib3.disable_warnings()					
	
	if len(proxy) == 1:
		if tor == True: #Manejo de errores de tor
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
		else: #Manejo de errores peticion normal
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
	else: #Mandejo de errores del proxy
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
					if tor == True: #Manejo de errores de tor
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
					else: #Manejo de errores peticion normal
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
			
				else: #Manejo de errores del proxy
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
		ver.append(v)
		ver.append('Version getting from configuration files')
		files(arg,verbose,v,cookies,headers,proxy,proxies,tor,report,ver)
		
	
def files(arg,verbose,version,cookies,headers,proxy,proxies,tor,report,ver): #Obtencion de plugins y temas
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	listThemes = ['//script/@src', '//@href']
	tmp = []
	readm = []
	change = []
	plug = []
	them = []
	rob = []
	requests.packages.urllib3.disable_warnings()					
	
	for row in reader:
		try:
			if 'Plugin' in row[1] and 'Ojs' in row[0]: # Se buscan plugins por defecto de los gestores de contenido
				plugin = arg + '/plugins' + row[2]
				
				if len(proxy) == 1:
					if tor == True: #Manejo de errores de tor
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

					else: #Manejo de errores peticion normal
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
			

				else: #Manejo de errores del proxy
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
									elif int(verbose) == 2:
										print "Plugin, Name: " + colored(pN.group(1),'green') + ' ,Path: ' + colored(plugin, 'green')
									elif int(verbose) == 3:
										print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green') + " " + colored(pV.group(2), 'blue')
									plug.append(pN.group(1))
									plug.append(plugin)
									plug.append(pV.group(2))
							except:
								if int(verbose) == 1:
									print "Plugin Name: " + colored(pN.group(1), 'green') 
								elif int(verbose) == 2 or int(verbose) == 3:
									print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green')		
								plug.append(pN.group(1))
								plug.append(plugin)
								plug.append('')
					except:
						continue
					
					regex = re.compile(r'(.*)\/(.*)\/README(.*)') # Archivos de configuracion visibles
					match = regex.search(plugin)
					try:
						if match.group():
							if int(verbose) == 1:
								print "Plugin Name: " + colored(match.group(2),'green')
							elif int(verbose) == 2 or int(verbose) == 3:
								print "Plugin, Name: " + colored(match.group(2), 'green') + ' ,Path: ' + colored(plugin, 'green')
							plug.append(match.group(2))
							plug.append(plugin)
							plug.append('')
					except:
						continue
				
				else:
					continue
			
			if int(verbose) == 3:
				if 'Readme' in row[1] and 'Ojs' in row[0]:
					readme = arg + '/docs/release-notes/README-' + row[2]
				
					if len(proxy) == 1:
						if tor == True: #Manejo de errores de tor
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

						else: #Manejo de errores peticion normal
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

					else: #Manejo de errores del proxy
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
						readm.append(readme)						
					else:
						continue
					
			
				elif 'Change' in row[1] and 'Ojs' in row[0]:	# Archivos de configuracion visibles
					changeLog = arg + '/docs/release-notes/ChangeLog-' + row[2]
				
					if len(proxy) == 1:
						if tor == True: #Manejo de errores de tor
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

						else: #Manejo de errores peticion normal
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
			

					else: #Manejo de errores del proxy
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
						change.append(changeLog)
					else:
						continue
	
				elif 'Robots' in row[1] and 'Ojs' in row[0]: # Archivos de configuracion visibles
				
					if len(proxy) == 1:
						if tor == True: #Manejo de errores de tor
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

						else: #Manejo de errores peticion normal
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
			

					else: #Manejo de errores del proxy
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
						rob.append(req.url)
					else:
						continue
			else:
				continue
		except:
			continue
	f.close()
	
	if len(proxy) == 1:
		if tor == True: #Manejo de errores de tor
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
		else: #Manejo de errores peticion normal
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
			

	else: #Manejo de errores del proxy
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
			elif int(verbose) == 2 or int(verbose) == 3:
				print colored( 'Default Theme', 'green') + ' Path: ' + colored(tmp[element], 'green')
			them.append('Default')
			them.append(tmp[element])
			element + i
		elif 'journals' in tmp[element]: #Tema journal
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group(): #Tema peronalizado
					if int(verbose) == 1:
						print colored('Customize Theme ', 'green')
					elif int(verbose) == 2:
						print colored('Customize Theme, Name: ' + match.group(2), 'green')
					elif int(verbose) == 3:	
						print 'Customize Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
					element + 1
					them.append('Customize Theme: ' + match.group(2))
					them.append(tmp[element])
			except:
				pass
		elif 'theme' in tmp[element]: 
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():
					if int(verbose) == 1:
						print 'Theme, Name: ' + colored(match.group(2),'green')
					elif int(verbose) == 2 or int(verbose) == 3:	
						print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
					them.append(match.group(2))
					them.append(tmp[element])
			except:
				pass	
		elif 'bootstrap' in tmp[element]: # Tema creado con bootstrap
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():	
					if int(verbose) == 1:
						print 'Theme, Name: ' + colored(match.group(2),'green')
					elif int(verbose) == 2 or int(verbose) == 3:
						print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
					them.append(match.group(2))
					them.append(tmp[element])
			except:
				pass	
		else:
			sys.exit
			readm = []
	
	vuln(version,verbose,report,arg,ver,plug,readm,change,rob,them,cookies,headers,proxy,proxies,tor)


def vuln(version,verbose,report,arg,ver,plug,readm,change,rob,them,cookies,headers,proxy,proxies,tor): # A partir de la version, se listan las posibles vulnerabilidades
	f = open('vuln','rb')
	reader = csv.reader(f,delimiter=',')
	
	vul = []
	
	for row in reader:
		try:
			if 'Ojs' in row[0] and row[1] in version:
				if int(verbose) == 1:
					print "Vulnerability Link: " + colored(row[3],'green')
				elif int(verbose) == 2 or int(verbose) == 3:
					print "Vulnerability Name: " + colored(row[2],'green') + ' ,Vulnerability Link: ' + colored(row[3],'green')
				vul.append(row[2]) #Usado para el reporte
				vul.append(row[3])
				vul.append(row[4])
				vul.append(row[5])
				vul.append(row[6])
			else:
				pass
		except IndexError:
			pass
	f.close()
	#rep(report,arg,ver,plug,readm,change,rob,them,vul)
	exploit(report,arg,ver,plug,readm,change,rob,them,vul,cookies,headers,proxy,proxies,tor)


def exploit(report,url,ver,plug,readm,change,rob,them,vul,cookies,headers,proxy,proxies,tor):
	rec = [] 
	ask = raw_input("There are some exploits in our DB that could be used in thi site, Do you want to try them? [Y/n]") or 'Y'
	if 'Y' in ask or 'y' in ask:
		ex = ['/classes/site/SiteDAO.inc.php','/classes/journal/JournalSettingsDAO.inc.php','/classes/scheduledTask/ScheduledTaskDAO.inc.php']
		succs = []
		for element in ex:
			t = url + element
			
			if len(proxy) == 1:
				if tor == True: #Manejo de errores de tor
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket
					error = """
				We are in trouble for some of the following reasons, please check them and try again :D
					- Something in the URL could be wrong.
					- The site is down.
					- It seems that we have problems using Tor :(
					"""
					try:
						r = requests.get(t,cookies = cookies, headers = headers,verify=False,timeout=10)
					except requests.RequestException:			
						print colored(error,'green')
						sys.exit(2)
					except:
						print colored(error,'green')
						sys.exit(2)
					
				else: #Manejo de errores peticion normal
					error = """
					We are in trouble for some of the following reasons, please check them and try again :D
						- Something in te URL could be wrong.
						- The site is down or doesn\'t exist.
					"""
					try:
						r = requests.get(t, cookies = cookies, headers = headers, verify=False,timeout=10)			
					except requests.RequestException:			
						print colored(error,'green')
						sys.exit(2)
					except:
						print colored(error,'green')
						sys.exit(2)
			else: #Manejo de errores del proxy
				error = """
				We are in trouble for some of the following reasons, please check them and try again :D
					- Something in te URL could be wrong.
					- The site is down or doesn\'t exist.
					- There\'s a problem with the proxy connection
				"""
				try:
					r = requests.get(t,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
				except requests.RequestException:		
					print colored(error,'green')
					sys.exit(2)
				except:
					print colored(error,'green')
					sys.exit(2)
			
			if int(r.status_code) == 200 and element in r.url: #Acceso al archivo
				succs.append(t)
			else:
				pass
		
		if len(succs) > 0:
			print colored('They were found the following vulnerabilities in the site, related with OS path','green')
			print colored(element,'yellow')
			print '\n'
			rec.append(element)
			#rep(report,ver,url,readm,change,pl,them,vul,rec)	
		else:
			print colored('Sorry there aren\'t any exploit available in the database','yellow')
			#rep(report,ver,url,readm,change,pl,them,vul,rec)	
	
	else:
		#rep(report,ver,url,readm,change,pl,them,vul,rec)
		sys.exit(2)

	

def rep(rep,url,ver,plug,readm,change,rob,them,vul): #Reporte

	title = ' *** Results of OJS Scanner***'
	execution =  ('Execution time was: %s seconds' % (time.time() - start_time))
	resource = 'Resource: ' + str(url)
	t = time.strftime('%d-%m-%Y')
	h = time.strftime('%H:%M:%S')
	
	for value in rep:
		if 'text' in value: #En texto plano
			fo = open(('OJSReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write(title.center(100) + '\n')
			fo.write('' + '\n')
			fo.write(execution.ljust(50) + '\n')
			fo.write('' + '\n')
			fo.write(resource.ljust(50) + '\n')
			fo.write('' + '\n')
			
			while len(ver) > 0:
				fo.write('Version: ' + ver[0] + '\n')
				fo.write('Path Version: ' + ver[1] + '\n')
				fo.write('' + '\n')
				ver.pop(1)
				ver.pop(0)
			
			if len(plug) == 0:
				pass
			else:
				fo.write('Plugins'.center(100) + '\n')
				fo.write('' + '\n')
				while len(plug) > 0:
					na = plug[0]
					pa = plug[1]
					ve = plug[2]
					if len(ve) > 0:
						ve = 'Version: ' + plug[2]
					else:
						ve = 'Version not found'
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Name: ' + na + '\n')
					fo.write('Path: ' + pa + '\n')
					fo.write(ve+ '\n')
					fo.write('' + '\n')
					plug.pop(2)
					plug.pop(1)
					plug.pop(0)
				
			if len(readm) == 0:
				pass
			else:
				fo.write('Readme Files'.center(100) + '\n')
				fo.write('' + '\n')
				while len(readm) > 0:
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Path: ' + readm[0] + '\n')
					fo.write('' + '\n')
					readm.pop(0)
				
			if len(change) == 0:
				pass
			else:
				fo.write('ChangeLog'.center(100) + '\n')
				fo.write('' + '\n')
				while len(change) > 0:
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Path: ' + change[0] + '\n')
					fo.write('' + '\n')
					change.pop(0)
				
			if len(rob) == 0:
				pass
			else:
				fo.write('Robots file'.center(100) + '\n')
				fo.write('' + '\n')
				while len(rob) > 0:
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Path: ' + rob[0] + '\n')
					fo.write('' + '\n')
					rob.pop(0)
				
			if len(them) == 0:
				pass
			else:
				fo.write('Theme(s) installed'.center(100) + '\n')
				fo.write('' + '\n')
				while len(them) > 0:
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write(them[0] + '\n')
					fo.write(them[1] + '\n')
					fo.write('' + '\n')
					them.pop(1)
					them.pop(0)
					
			if len(vul) == 0:
				pass
			else:
				fo.write('Vulnerabilities found'.center(100) + '\n')
				fo.write('' + '\n')
				while len(vul) > 0:
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Vulnerability Name: ' + vul[0] + '\n')
					fo.write('Vulnerability Link: ' + vul[1] + '\n')
					fo.write('Description: ' + vul[2] + '\n')
					fo.write('Recomendation: ' + vul[3] + '\n')
					fo.write('CVSS: ' + vul[4] + '\n')
					fo.write('' + '\n')
					vul.pop(4)
					vul.pop(3)
					vul.pop(2)
					vul.pop(1)
					vul.pop(0)
			
			fo.close()
		elif 'html'.upper() in value or 'html' in value: #HTML
			fo = open(('OJSReport_' + t + '_'+ h + '.html'), 'wb')
			
			header = """
			<html>
			<head>
			<style>
			table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
				width: 100%;
			}
	
			td, th {
				border: 3px solid #808080;
				text-align: center;
				padding: 8px;
			}

			tr:nth-child(even) {
				background-color: #f8f8ff;
			}
			</style>

				<title>OJS Results</title>
			</head>
			<body text = "B8860B"; link ="B8860B"; bgcolor="00008B">
				<h1 align="center">Results of OJS Scanner</h1><br><br>
			"""
			fo.write( header)
			fo.write("""<h1 align="left"> %s </h1>""" % execution)
			fo.write("""<h1 align="left"><a href='%s'> %s </a></h1><br>""" % (url,resource))
			
			while len(ver) > 0:
				fo.write("""<h1 align="left"> Version: %s </h1><br>""" % ver[0])
				ver.pop(1)
				ver.pop(0)
			
			if len(plug) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Plugins </h1><br>""")
				fo.write("""<table>
							<tr>
								<th>Name</th>
								<th>Path</th>
								<th>Version</th>
							</tr>
						""")
				while len(plug) > 0:
					na = plug[0]
					pa = plug[1]
					ve = plug[2]
					if len(ve) > 0:
						ve =  plug[2]
					else:
						ve = 'Version not found'
					
					fo.write("""
							<tr>
								<th>%s</th>
								<th><a href='%s'> %s </a></th>
								<th>%s</th>
							</tr>
							""" % (na,pa,pa,ve))
					plug.pop(2)
					plug.pop(1)
					plug.pop(0)
				fo.write("""</table><br>""")
			
			if len(readm) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Readme Files </h1><br>""")
				fo.write("""<table>	""")
				while len(readm) > 0:
					fo.write("""<tr>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (readm[0],readm[0]))
					
					readm.pop(0)
				fo.write("""</table><br>""")
						
			
			
			if len(change) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> ChangeLog </h1><br>""")
				fo.write("""<table>	""")
				while len(change) > 0:
					fo.write("""<tr>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (change[0],change[0]))
					change.pop(0)
				fo.write("""</table><br>""")
				
				
			if len(rob) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Robots File </h1><br>""")
				fo.write("""<table>	""")
				while len(rob) > 0:
					fo.write("""<tr>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (rob[0],rob[0]))
					rob.pop(0)
				fo.write("""</table><br>""")
				
			if len(them) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Theme(s) installed </h1><br>""")
				fo.write("""<table>
							<tr>
								<th>Name</th>
								<th>Path</th>
							</tr>""")
				while len(them) > 0:
					fo.write("""<tr>
									<th>%s</th>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (them[0],them[1],them[1]))
					them.pop(1)
					them.pop(0)
				fo.write("""</table><br>""")
				
					
			if len(vul) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Vulnerabilities found </h1><br>""")
				fo.write("""<table>
							<tr>
								<th>Name</th>
								<th>Link</th>
								<th>Description</th>
								<th>Recomendation</th>
								<th>CVSS</th>
							</tr>""")
				while len(vul) > 0:
					fo.write("""
							<tr>
								<th>%s</th>
								<th><a href='%s'> %s </a></th>
								<th>%s</th>
								<th><a href='%s'> %s </a></th>
								<th>%s</th>
							</tr>""" % (vul[0],vul[1],vul[1],vul[2],vul[3],vul[3],vul[4]))
					
					vul.pop(4)
					vul.pop(3)
					vul.pop(2)
					vul.pop(1)
					vul.pop(0)
				fo.write("""</table><br>""")
			fo.write("""
			</body>
			</html>""")
			fo.close()
		
		elif 'xml'.upper() in value or 'xml' in value:	#XML
			fo = open(('OJSReport_' + t + '_'+ h + '.xml'), 'wb')
			
			fo.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
			fo.write('<?xml-stylesheet type="text/css" href="ojs.css"?>' + '\n')
			fo.write('<ojsScan>' + '\n')
			fo.write('	<title>***Results of OJS Scanner***</title><br />' + '\n')
			fo.write(' 	<time>%s</time>' % execution)
			fo.write('	<resource>%s</resource>' % resource)
			
			while len(ver) > 0:
				fo.write(	'<version>Version: %s</version>' % ver[0] + '\n') 
				ver.pop(1)
				ver.pop(0)
			
			
			
			
			if len(plug) == 0:
				pass
			else:
				fo.write(	'<subtitle>Plugins</subtitle>' + '\n')
				while len(plug) > 0:
					na = plug[0]
					pa = plug[1]
					ve = plug[2]
					if len(ve) > 0:
						ve =  plug[2]
					else:
						ve = 'Version not found'
					fo.write(	'<plugin>')
					fo.write(		'<name>%s</name>' % (na))
					fo.write(		'<path>%s</path>' % (pa))
					fo.write(		'<pversion>%s</pversion>' % (ve))
					fo.write(	'</plugin>')
					plug.pop(2)
					plug.pop(1)
					plug.pop(0)
			
					
			
			
			if len(readm) == 0:
				pass
			else:
				fo.write(	'<subtitle>Readme Files</subtitle>' + '\n')
				while len(readm) > 0:
					fo.write(	'<readme>')
					fo.write(		'<rpath>%s</rpath>' % (readm[0]))	
					fo.write(	'</readme>')
					readm.pop(0)
						
			
			if len(change) == 0:
				pass
			else:
				fo.write(	'<subtitle>ChangeLog Files</subtitle>' + '\n')
				while len(change) > 0:
					fo.write(	'<changeLog>')
					fo.write(		'<cpath>%s</cpath>' % (change[0]))	
					fo.write(	'</changeLog>')
					change.pop(0)
				
			if len(rob) == 0:
				pass
			else:
				fo.write(	'<subtitle>Robots Files</subtitle>' + '\n')
				while len(rob) > 0:
					fo.write(	'<robots>')
					fo.write(		'<ropath>%s</ropath>' % (rob[0]))	
					fo.write(	'</robots>')
					rob.pop(0)
			
			if len(them) == 0:
				pass
			else:
				fo.write(	'<subtitle>Theme</subtitle>' + '\n')
				while len(them) > 0:
					fo.write(	'<theme>')
					fo.write(		'<tname>%s</tname>' % (them[0]))
					fo.write(		'<tpath>%s</tpath>' % (them[1]))
					fo.write(	'</theme>')
					them.pop(1)
					them.pop(0)
		
			if len(vul) == 0:
				pass
			else:
				fo.write(	'<subtitle>Vulnerabilities found</subtitle>' + '\n')
				while len(vul) > 0:
					fo.write(	'<vulnerability>')
					fo.write(		'<vname>%s</vname>' % vul[0])
					fo.write(		'<vlink>%s</vlink>' % vul[1])
					fo.write(		'<description>%s</description>' % vul[2])
					fo.write(		'<recomendation>%s</recomendation>' % vul[3])
					fo.write(		'<cvss>%s</cvss>' % vul[4])
					fo.write(	'</vulnerability>')
					vul.pop(4)
					vul.pop(3)
					vul.pop(2)
					vul.pop(1)
					vul.pop(0)
		
			fo.write('</ojsScan>')
			fo.close()
					
				
				
			
		else:
			pass

