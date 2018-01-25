import re # Utilizado para las regex
import sys
import requests # Utilizado para realizar las peticiones
import hashlib # Utilizado para obtener los hashes
from lxml import etree # Utilizado para obtener los enlaces, imagenes, etc.
from lxml import html # Utilizado para obtener los enlaces, imagenes, etc.
import wget # Utilizado para descargar las imagenes
import os 
import time
from collections import Counter # Utilizado para obtener el promedio de las versiones
import operator
from termcolor import colored
import csv # Utilizado para leer los archivos que contienen los hashes
import socks #Tor
import socket #Tor
import random
import time

plugins = ['']
start_time = time.time() #Tiempo de ejecucion del programa
def moodle(arg, verbose,cookie,agent,proxip,proxport,tor,report,th): # Version
	print colored("\nBeginning moodle scanner", 'yellow')
	requests.packages.urllib3.disable_warnings()
	
	if 'http' in arg:
		if '.php' in arg: #Validacion de la pagina principal del sitio
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
	
	
	if len(proxy) == 1:
		if tor == True: # Peticiones a traves de Tor
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
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
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
				
	else: # Peticiones a traves del proxy
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
		
		if cookie is None: #Cookie aleatoria
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

	m = hashlib.md5()
	
	if 'yui_combo' in req.text: #Validacion del moodle
		pass
	else:
		print colored('The site: ','green') + colored(arg,'yellow') + colored(' isn\'t a moodle','green')
		sys.exit(2)
	
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
				upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,verify=False,timeout=10)
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
				upgrade = requests.get(arg + '/lib/upgrade.txt', cookies = cookies, headers = headers,verify=False,timeout=10)			
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
			upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
						
	if int(upgrade.status_code) == 200: #Si tiene el archivo upgrade
		regex = re.compile(r'===(.*)===')
		match = regex.search(upgrade.text)
		try:
			if match.group(): #Si es un numero de version
				if 'Slideshow section start here' in match.group(1):
					version(arg,verbose,cookies,headers,proxy,proxies,tor,report,l)
					
				else:
					if int(verbose) == 1:
						print 'Version site: ' + colored(match.group(1),'green')
						
					elif int(verbose) == 2:
						print "Version site: " + colored(arg,'green') + "is: " + colored(match.group(1),'green')
					elif int(verbose) == 3:
						print "Version site: " + colored(arg,'green') + "is: " + colored(match.group(1),'green')
						print "Version site found it in: " + colored(upgrade.url,'green')
						
					ver.append(match.group(1))
					ver.append(upgrade.url)
					files(arg,verbose,match.group(1),cookies,headers,proxy,proxies,tor,report,ver) # Si existe el archivo se obtienen los plugins y el tema
				
					
		except:
			exit(2)
		
	else: #Si no lo tiene
		version(arg,verbose,cookies,headers,proxy,proxies,tor,report,ver) # Si no se obtiene la version a partir del archivo, se obtiene a partir de los archivos por defecto
					

def version(arg,verbose,cookies,headers,proxy,proxies,tor,report,ver):	 # Obtencion de la version a partir de archivos
	print colored('We\'re trying to get the version through default files, please wait','green')
	m = hashlib.md5()
	elements = []
	ver = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href'] # Busqueda de imagenes, favicon, hojas de estilo y js
	
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
				res = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
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
				res = requests.get(arg, cookies = cookies, headers = headers, verify=False,timeout=10)			
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
			res = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
		
	webpage = html.fromstring(res.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)): # Busqueda de css, js, imagenes, favicon
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				if link.startswith('http'):	
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
						
					if req.status_code == 200 and i in range(2,3): # Si existen las imagenes, se descargan y se obtiene el hash
						try:
							filename = wget.download(link, bar=None)
							m.update(filename)
							hs = m.hexdigest()
							elements.append(hs)
							os.remove(filename)
						except:
							continue
				
					else:
						try: # Si es js o css, se obtiene el has
							m.update(req.text)
							hs =  m.hexdigest()
							elements.append(hs)
						except:
							continue
	
	if len(proxy) == 1: # Obtencion del hash del archivo README
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
				readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,verify=False,timeout=10)
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
				readme = requests.get(arg + '/README.txt', cookies = cookies, headers = headers, verify=False,timeout=10)			
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
			readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
			
	if readme.status_code == 200:
		try:
			m.update(readme.text)
			hs = m.hexdigest()
			elements.append(hs)
		except:
			pass
		
	
	
	f = open('versions','rb')	 # Comparacion de los hashes, con la lista de hashes por defecto	
	reader = csv.reader(f,delimiter=',')
			
	for element in elements:
		for row in reader:
			try:
				if element in row[2] and 'Moodle' in row[0]:
					average.append(row[1])
			except:
				continue
	
	cnt = Counter(average) # Calculo de la version que mas veces se repite
		
		
	if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
		try:
			v = max(cnt.iteritems(),key=operator.itemgetter(1))[0]
		except:
			print colored('Sorry, It couldn\'t get the version of the Moodle, please try again later :(','green')
			sys.exit(2)
		
		print '\nVersion getting from configuration files: ' + colored(v, 'green')
		test = unicode(v)
		ver.append(v)
		ver.append('Version getting from configuration files')
		files(arg,verbose,test,cookies,headers,proxy,proxies,tor,report,ver) # Obtencion de plugins y temas
		f.close()
		
		

def files(arg, verbose,version,cookies,headers,proxy,proxies,tor,report,ver): # Obtencion de plugins y temas
	readm = []
	change = []
	pl = []
	them = []
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		try:
			if int(verbose) == 3: # Busqueda de archivos de configuracion visibles
				if 'Readme' in row[1] and 'Moodle' in row[0]: 
					readme = arg + row[2]
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
						error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
						try:
							req = requests.get(readme,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)						
						except requests.RequestException:					
							print colored(error,'green')
							sys.exit(2)
						except:
							print colored(error,'green')
							sys.exit(2)
				
					if req.status_code == 200: #Si se tiene acceso al archivo
						print 'README file: ' + colored(readme, 'green')
						readm.append('2')
						readm.append(readme)
					elif req.status_code == 403: #Si el archivo existe pero no se tiene acceso
						print 'Forbidden README: ' + colored(readme, 'green')
						readm.append('4')
						readm.append(readme)
					else:
						continue
		
				elif 'Change' in row[1] and 'Moodle' in row[0]: # Busqueda de archivos de configuracion visibles
					changeLog = arg +  row[2]
				
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
				
					if req.status_code == 200: #Si existe el archivo
						print 'ChangeLog: ' + colored(changeLog,'green')
						change.append('2')
						change.append(changeLog)
					elif req.status_code == 403: #Si existe el archivo pero no se tiene acceso al mismo
						print 'Forbidden ChangeLog: ' + colored(changeLog,'green')
						change.append('4')
						change.append(changeLog)
					else:
						continue
			else:
				pass
				
			if 'Plugin' in row[1] and 'Moodle' in row[0]: # Busqueda de los plugins
				plugin = arg + row[2]
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
				
				if req.status_code == 200: # Obtencion de la version del plugin
					up = re.sub(r'\/upgrade.txt','',row[2])
					begin = re.sub(r'^\/','',up)
					regex = re.compile(r'(===)(.*)(===)')
					match = regex.search(req.text)
					try:
						path = re.sub(r'upgrade.txt','',plugin)
						if match.group():
							try:
								if complex(match.group(2)):
									if int(verbose) == 1:
										print "Plugin Name: " + colored(begin, 'green')
									elif int(verbose) == 2:
										print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path,'green')
									elif int(verbose) == 3:
										print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path, 'green') + ' ,Version: ' + colored(match.group(2),'blue')
									pl.append(begin)
									pl.append(path)
									pl.append(match.group(2))
							except:
								if int(verbose) == 1:
									print "Plugin Name: " + colored(begin, 'green')
								elif int(verbose) == 2 or int(verbose) == 3:
									print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path, 'green')
								pl.append(begin)
								pl.append(path)
								pl.append('')
					except:
						continue
		
				elif req.status_code == 403: #Exitencia del plugin, sin acceso al archivo
					path = re.sub(r'upgrade.txt','',plugin)
					one = re.sub(r'^\/','',element)
					plug = re.sub(r'/upgrade.txt','',one)
					if int(verbose) == 3:
						print "Forbidden Plugin,  Name: " + colored(plug, 'yellow') + ', Path: ' + colored(path, 'green')
						pl.append(plug)
						pl.append(path)
						pl.append('4')
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
				res = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
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
				res = requests.get(arg, cookies = cookies, headers = headers, verify=False,timeout=10)			
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
			res = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)		
		except requests.RequestException:		
			print colored(error,'green')
			sys.exit(2)
		except:
			print colored(error,'green')
			sys.exit(2)
	
	webpage = html.fromstring(res.text)
	theme =  webpage.xpath('//link[@rel="shortcut icon"]/@href') # Busqueda del tema a partir del favicon
	
	for element in theme:
		if '=' in element:
			regex = re.compile(r'(.*)(theme=)(.*)(\&image=(.*))')
			match = regex.search(element)
			try:
				if match.group():
					if int(verbose) == 1:
						print "Theme Name: " + colored(match.group(3), 'green')
					elif int(verbose) == 2 or int(verbose) == 3:
						print "Theme Name: " + colored(match.group(3), 'green') + ', Path: ' + colored(element, 'green')
					them.append(match.group(3))
					them.append(element)
			except:
				pass
		else:
			regex = re.compile(r'(.*)\/(.*)\/theme\/(.*)')
			match = regex.search(element)
			try:
				if match.group():
					if int(verbose) == 1:
						print "Theme Name: " + colored(match.group(2),'green')
					elif int(verbose) == 2 or int(verbose) == 3:
						print "Theme Name: " + colored(match.group(2), 'green') + ', Path: ' + colored(match.group(1) + '/' + match.group(2), 'green')
					them.append(match.group(2))
					them.append(match.group(1) + '/' + match.group(2))
			except:
				if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
					print "Theme Name: " + colored(match.group(2), 'green')
					print match.group(2)
				them.append(match.group(2))
				them.append('It can\'t get the path')
					
	vuln(version,verbose,report,ver,arg,readm,change,pl,them,cookies,headers,proxy,proxies,tor)
	
def vuln(version,verbose,report,ver,arg,readm,change,pl,them,cookies,headers,proxy,proxies,tor): # Listado de vulnerabilidades obtenidas a partir de la version del gestor de contenidos
	vul = []
	f = open('vuln','rb')
	reader = csv.reader(f,delimiter='|')
	
	for row in reader:
		try:
			if 'Moodle' in row[0] and row[1] in version:
				if int(verbose) == 1:
					print "Vulnerability Link: " + colored(row[3],'green')
				elif int(verbose) == 2 or int(verbose) == 3:
					print "Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + row[3]
				vul.append(row[2]) #Utilizado para el reporte
				vul.append(row[3])
				vul.append(row[4])
				vul.append(row[5])
				vul.append(row[6])
			else:
				pass
		except IndexError:
			pass
			
	f.close()
	exploit(report,ver,arg,readm,change,pl,them,vul,cookies,headers,proxy,proxies,tor)
	

def exploit(report,ver,url,readm,change,pl,them,vul,cookies,headers,proxy,proxies,tor): #Explotacion de algunas vulnerabilidades
	rec = [] 
	ask = raw_input("There are some exploits in our DB that could be used in thi site, Do you want to try them? [Y/n]") or 'Y'
	if 'Y' in ask or 'y' in ask:
		ex = ['/admin/roles/usersroles.php?userid=6&','/admin/mnet/trustedhosts.html','/lib/ajax/getnavbranch.php?id=6&type=6','/lib/phpunit/bootstrap.php','/blog/rsslib.php','/admin/cron.php','/iplookup/index.php']
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
				if len(r.content) > 0: #Si devuelve algun valor
					if '!!!' in r.content:
						pass
					else:
						succs.append(t)
				else:
					pass
			elif int(r.status_code) == 404 and 'courseid' in r.content:
				succs.append(t)
		
		if len(succs) > 0:
			for element in succs: #Recomendaciones para realizar la explotacion
				if 'iplookup' in element or 'cron' in element:
					print colored('They were found the following vulnerabilities in the site, related with a DoS attack','green')
					print colored(element,'yellow')
					print '\n'
					rec.append('dos')
					rec.append(element)
				elif 'rsslib' in element or 'bootstrap' in element:
					print colored('They were found the following vulnerabilities in the site, related with OS path','green')
					print colored(element,'yellow')
					print '\n'
					rec.append('os')
					rec.append(element)
				elif 'ajax' in element or 'usersroles' in element:
					print colored('They were found the following vulnerabilities in the site, related with Obtain Information about users and courses in the site','green')
					print colored(element,'yellow')
					print '\n'
					rec.append('list')
					rec.append(element)
				elif '.html' in element:
					print colored('They were found the following vulnerabilities in the site, related with upload files','green')
					print colored(element,'yellow')
					print '\n'
					rec.append('up')
					rec.append(element)
			rep(report,ver,url,readm,change,pl,them,vul,rec)	
		else:
			print colored('Sorry there aren\'t any exploit available in the database','yellow')
			rep(report,ver,url,readm,change,pl,them,vul,rec)	
	
	else:
		rep(report,ver,url,readm,change,pl,them,vul,rec)
	
	

def rep(rep,version,url,readme,change,pl,them,vul,rec): #reporte
	title = ' *** Moodle Results ***'
	execution =  ('Execution time was: %s seconds' % (time.time() - start_time))
	resource = 'Resource: ' + str(url)
	t = time.strftime('%d-%m-%Y')
	h = time.strftime('%H:%M:%S')
	
	for value in rep:
		if 'text' in value:	#Texto plano
			fo = open(('MoodleReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write(title.center(100) + '\n')
			fo.write('' + '\n')
			fo.write(execution.ljust(50) + '\n')
			fo.write('' + '\n')
			fo.write(resource.ljust(50) + '\n')
			fo.write('' + '\n')
			
			while len(version) > 0:
				fo.write('Version: ' + version[0] + '\n')
				fo.write('Path Version: ' + version[1] + '\n')
				fo.write('' + '\n')
				version.pop(1)
				version.pop(0)
				
			if len(pl) == 0:
				pass
			else:
				fo.write('Plugins'.center(100) + '\n')
				fo.write('' + '\n')
				while len(pl) > 0:
					na = pl[0]
					pa = pl[1]
					ve = pl[2]
					if len(ve) > 0:
						ve = 'Version: ' + pl[2]
					else:
						ve = 'Version not found'
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Name: ' + na + '\n')
					fo.write('Path: ' + pa + '\n')
					fo.write(ve+ '\n')
					fo.write('' + '\n')
					pl.pop(2)
					pl.pop(1)
					pl.pop(0)
			
			if len(readme) == 0:
				pass
			else:
				fo.write('Readme Files'.center(100) + '\n')
				fo.write('' + '\n')
				while len(readme) > 0:
					if int(readme[0]) == 2:
						fo.write('-----------------------------------------------------------------------------------\n')
						fo.write('Status code: 200\n')
						fo.write('Path: ' + readme[1] + '\n')
						fo.write('' + '\n')
						readme.pop(1)
						readme.pop(0)
					elif int(readme[0]) == 4:
						fo.write('-----------------------------------------------------------------------------------\n')
						fo.write('Forbidden file\n')
						fo.write('Path: ' + readme[1] + '\n')
						fo.write('' + '\n')
						readme.pop(1)
						readme.pop(0)
					else:
						pass
			
			if len(change) == 0:
				pass
			else:
				fo.write('ChangeLog'.center(100) + '\n')
				fo.write('' + '\n')
				while len(change) > 0:
					if int(change[0]) == 2:
						fo.write('-----------------------------------------------------------------------------------\n')
						fo.write('Status code: 200\n')
						fo.write('Path: ' + change[1] + '\n')
						fo.write('' + '\n')
						change.pop(1)	
						change.pop(0)
					elif int(change[0]) == 4:
						fo.write('-----------------------------------------------------------------------------------\n')
						fo.write('Forbidden file\n')
						fo.write('Path: ' + change[1] + '\n')
						fo.write('' + '\n')
						change.pop(1)	
						change.pop(0)
					else:
						pass
			
				
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
			
			if len(rec) == 0:
				pass
			else:
				fo.write('Exploits'.center(100) + '\n')
				fo.write('' + '\n')
				while len(rec) > 0:		
					fo.write('-----------------------------------------------------------------------------------\n')
					fo.write('Path to exploit: ' + rec[1] + '\n')
					if 'dos' in rec[0]:			
						fo.write('You could exploit this vulnerability by requesting the same resource multiple times \n')
						fo.write('' + '\n')
						rec.pop(1)
						rec.pop(0)
					elif 'list' in rec[0]:
						fo.write('With this vulnerability you could listing information about users, courses and information contain in the database by changing the number in the ID parameter \n')
						fo.write('' + '\n')
						rec.pop(1)
						rec.pop(0)
					elif 'up' in rec[0]:
						fo.write('It\'s possible to upload files with this vulnerability \n')
						fo.write('' + '\n')
						rec.pop(1)
						rec.pop(0)
					elif 'os' in rec[0]:
						fo.write('You could get the installation path in the response of the resourse\n')
						fo.write('' + '\n')
						rec.pop(1)
						rec.pop(0)
			fo.close()
		elif 'html'.upper() in value or 'html' in value: #HTML
			fo = open(('MoodleReport_' + t + '_'+ h + '.html'), 'wb')
			
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
				<h1 align="center">Results of Moodle Scanner</h1><br><br>
			"""
			fo.write( header)
			fo.write("""<h1 align="left"> %s </h1>""" % execution)
			fo.write("""<h1 align="left"><a href='%s'> %s </a></h1><br>""" % (url,resource))
			
			
			while len(version) > 0:
				fo.write("""<h1 align="left"> Version: %s </h1><br>""" % version[0])
				version.pop(1)
				version.pop(0)
				
				
			if len(pl) == 0:
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
				while len(pl) > 0:
					na = pl[0]
					pa = pl[1]
					ve = pl[2]
					if len(ve) > 0:
						ve =  pl[2]
					else:
						ve = 'Version not found'
					
					fo.write("""
							<tr>
								<th>%s</th>
								<th><a href='%s'> %s </a></th>
								<th>%s</th>
							</tr>
							""" % (na,pa,pa,ve))
					pl.pop(2)
					pl.pop(1)
					pl.pop(0)
				fo.write("""</table><br>""")
			
			if len(readme) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Readme Files </h1><br>""")
				fo.write("""<table>	
								<tr>
									<th>Status code</th>
									<th>Path</th>
								</tr>""")
				while len(readme) > 0:
					if int(readme[0]) == 2:
						fo.write("""<tr>
									<th>200 OK!</th>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (readme[1],readme[1]))
						readme.pop(1)
						readme.pop(0)
						
					elif int(readme[0]) == 4:
						fo.write("""<tr>
									<th>403 Forbidden File</th>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (readme[1],readme[1]))
						readme.pop(1)
						readme.pop(0)
					
				fo.write("""</table><br>""")
						
				
			if len(change) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> ChangeLog </h1><br>""")
				fo.write("""<table>	
								<tr>
									<th>Status code</th>
									<th>Path</th>
								</tr>""")
				while len(change) > 0:
					if int(change[0]) == 2:
						fo.write("""<tr>
									<th>200 OK!</th>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (change[1],change[1]))
						change.pop(1)
						change.pop(0)
						
					elif int(change[0]) == 4:
						fo.write("""<tr>
									<th>403 Forbidden File</th>
									<th><a href='%s'> %s </a></th>
								</tr>""" % (change[1],change[1]))
						change.pop(1)
						change.pop(0)
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
				
			if len(rec) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Exploits found </h1><br>""")
				fo.write("""<table>
							<tr>
								<th>Path</th>
								<th>Description</th>
							</tr>""")
					
				while len(rec) > 0:
					if 'dos' in rec[0]:			
						fo.write("""<tr>
										<th><a href='%s'> %s </a></th>
										<th>You could exploit this vulnerability by requesting the same resource multiple times</th>
									</tr>""" % (rec[1],rec[1]))
						rec.pop(1)
						rec.pop(0)
						
					elif 'list' in rec[0]:
						fo.write("""<tr>
										<th><a href='%s'> %s </a></th>
										<th>With this vulnerability you could listing information about users, courses and information contain in the database by changing the number in the ID parameter</th>
									</tr>""" % (rec[1],rec[1]))
						rec.pop(1)
						rec.pop(0)
					elif 'up' in rec[0]:
						fo.write("""<tr>
										<th><a href='%s'> %s </a></th>
										<th>It\'s possible to upload files with this vulnerability</th>
									</tr>""" % (rec[1],rec[1]))
						rec.pop(1)
						rec.pop(0)
					elif 'os' in rec[0]:
						fo.write("""<tr>
										<th><a href='%s'> %s </a></th>
										<th>You could get the installation path in the response of the resourse</th>
									</tr>""" % (rec[1],rec[1]))
						rec.pop(1)
						rec.pop(0)
					
			fo.write("""</table><br>""")	
			fo.write("""
			</body>
			</html>""")
			fo.close()

		elif 'xml'.upper() in value or 'xml' in value:	#XML
			fo = open(('MoodleReport_' + t + '_'+ h + '.xml'), 'wb')

			fo.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
			fo.write('<?xml-stylesheet type="text/css" href="moodle.css"?>' + '\n')
			fo.write('<moodleScan>' + '\n')
			fo.write('	<title>***Results of Moodle Scanner***</title><br />' + '\n')
			fo.write(' 	<time>%s</time>' % execution)
			fo.write('	<resource>%s</resource>' % resource)
			
			
			
			while len(version) > 0:
				fo.write(	'<version>Version: %s</version>' % version[0] + '\n') 
				version.pop(1)
				version.pop(0)
			
			if len(pl) == 0:
				pass
			else:
				fo.write(	'<subtitle>Plugins</subtitle>' + '\n')
				while len(pl) > 0:
					na = pl[0]
					pa = pl[1]
					ve = pl[2]
					if len(ve) > 0:
						ve =  pl[2]
					else:
						ve = 'Version not found'
					fo.write(	'<plugin>')
					fo.write(		'<name>%s</name>' % (na))
					fo.write(		'<path>%s</path>' % (pa))
					fo.write(		'<pversion>%s</pversion>' % (ve))
					fo.write(	'</plugin>')
					pl.pop(2)
					pl.pop(1)
					pl.pop(0)
			
							
			if len(readme) == 0:
				pass
			else:
				fo.write(	'<subtitle>Readme Files</subtitle>' + '\n')
				while len(readme) > 0:
					if int(readme[0]) == 2:
						fo.write(	'<readme>')
						fo.write(		'<codeOk>%s</codeOk>' % (readme[1]))
						fo.write(	'</readme>')
						readme.pop(1)
						readme.pop(0)
					elif int(readme[0]) == 4:
						fo.write(	'<readme>')
						fo.write(		'<forbidden>%s</forbidden>' % (readme[1]))
						fo.write(	'</readme>')
						readme.pop(1)
						readme.pop(0)
			
			if len(change) == 0:
				pass
			else:
				fo.write(	'<subtitle>ChangeLog Files</subtitle>' + '\n')
				while len(change) > 0:
					if int(change[0]) == 2:
						fo.write(	'<changeLog>')
						fo.write(		'<codeOk>%s</codeOk>' % (change[1]))
						fo.write(	'</changeLog>')
						change.pop(1)
						change.pop(0)
					elif int(change[0]) == 4:
						fo.write(	'<changeLog>')
						fo.write(		'<forbidden>%s</forbidden>' % (change[1]))
						fo.write(	'</changeLog>')
						change.pop(1)
						change.pop(0)
			
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
				for element in vul:
					if len(element) < 7:
						fo.write(	'<vul>%s</vul>' % element)
						fo.write(	'<vul>-----------------------------------------</vul>')
					else:
						fo.write(	'<vul>%s</vul>' % element)
			
			
			if len(rec) == 0:
				pass
			else:
				while len(rec) > 0:
					
					if 'dos' in rec[0]:	
						if '&'	in rec[1]:
							t = rec[1].replace('&',"&amp;")
						else:
							t = rec[1]
						fo.write(	'<exploit>')
						fo.write(		'<epath>%s</epath>' % t)
						fo.write(		'<description>You could exploit this vulnerability by requesting the same resource multiple times</description>')
						fo.write(	'</exploit>')
						rec.pop(1)
						rec.pop(0)
						
					elif 'list' in rec[0]:
						if '&'	in rec[1]:
							t = rec[1].replace('&',"&amp;")
						else:
							t = rec[1]
						fo.write("""<exploit>""")
						fo.write("""<path>"%s"</path>""" % t)
						fo.write("""<description>With this vulnerability you could listing information about users, courses and information contain in the database by changing the number in the ID parameter</description>""")
						fo.write("""</exploit>""")
						rec.pop(1)
						rec.pop(0)
						
					elif 'up' in rec[0]:
						if '&'	in rec[1]:
							t = rec[1].replace('&',"&amp;")
						else:
							t = rec[1]
						fo.write("""<exploit>""")
						fo.write("""<path>"%s"</path>""" % t)
						fo.write("""<description>It's possible to upload files with this vulnerability</description>""")
						fo.write("""</exploit>""")
						rec.pop(1)
						rec.pop(0)
							
					elif 'os' in rec[0]:
						if '&'	in rec[1]:
							t = rec[1].replace('&',"&amp;")
						else:
							t = rec[1]
						fo.write("""<exploit>""")
						fo.write("""<path>"%s"</path>""" % t)
						fo.write("""<description>You could get the installation path in the response of the resourse</description>""")
						fo.write("""</exploit>""")
						rec.pop(1)
						rec.pop(0)


						
			fo.write('</moodleScan>')
			fo.close()
			
		else:
			pass

				
