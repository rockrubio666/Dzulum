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

plugins = ['']

def moodle(arg, verbose,cookie,agent,proxip,proxport,tor,report): # Version
	requests.packages.urllib3.disable_warnings()
	
	if 'http' in arg:
		req = requests.get(arg,verify=False)
		if '.php' in arg:
			ind = raw_input('If you don\'t introduce the principal page, you couldn\'t get enough evidence. Do yo want to continue? [y/N] ') or 'N'
			if 'Y' in ind or 'y' in ind:
				pass
			else:
				print colored('Check the URL and try again :D ', 'green')
				sys.exit(2)
		if 'yui_combo' in req.text:
			pass
		else:
			print colored('The site: ','green') + colored(arg,'yellow') + colored(' isn\'t a moodle','green')
			sys.exit(2)
	else:
		print colored('The URL doesn\'t have http or https, please check it and try again :D ','green')
		sys.exit(2)
		
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	l = []
	
	
	if len(proxy) == 1:
		if tor == True: # Peticiones a traves de Tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				req = requests.get(arg,verify=False,timeout=10)
			except requests.RequestException:
				error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down.
		- It seems that we have problems using Tor :(
"""
				print colored(error,'green')
				sys.exit(2)
			
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)

		else:
			try:
				req = requests.get(arg,verify=False,timeout=10)
			except requests.RequestException:
				error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
"""
				print colored(error,'green')
				sys.exit(2)
			
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
	else: # Peticiones a traves del proxy
		try:
			req = requests.post(arg,proxies = proxies,verify=False,timeout=10)
		except requests.RequestException:
			error = """
	We are in trouble for some of the following reasons, please check them and try again :D
		- Something in te URL could be wrong.
		- The site is down or doesn\'t exist.
		- There\'s a problem with the proxy connection
"""
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

	m = hashlib.md5()
	
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
		else:
			try:
				upgrade = requests.get(arg + '/lib/upgrade.txt', cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
	else:
		try:
			upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
		except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
						
	if int(upgrade.status_code) == 200: #Si tiene el archivo upgrade
		regex = re.compile(r'===(.*)===')
		match = regex.search(upgrade.text)
		try:
			if match.group(): #Si es un numero de version
				if 'Slideshow section start here' in match.group(1):
					version(arg,verbose,cookies,headers,proxy,proxies,tor,report,l)
					sys.exit(2)
				else:
					if int(verbose) == 1:
						print 'Version site: ' + colored(match.group(1),'green')
						l.append('Version site: ' + match.group(1))
					elif int(verbose) == 2:
						print "Version site: " + colored(arg,'green') + "is: " + colored(match.group(1),'green')
						l.append("Version site: " + arg + "is: " + match.group(1))
					elif int(verbose) == 3:
						print "Version site: " + colored(arg,'green') + "is: " + colored(match.group(1),'green')
						print "Version site found it in: " + colored(upgrade.url,'green')
						l.append("Version site: " + arg + "is: " + match.group(1) + "Found it in: " + upgrade.url)
					files(arg,verbose,match.group(1),cookies,headers,proxy,proxies,tor,report,l) # Si existe el archivo se obtienen los plugins y el tema
				
					
		except:
			exit(2)
		
	else: #Si no lo tiene
		version(arg,verbose,cookies,headers,proxy,proxies,tor,report,l) # Si no se obtiene la version a partir del archivo, se obtiene a partir de los archivos por defecto
					

def version(arg,verbose,cookies,headers,proxy,proxies,tor,report,l):	 # Obtencion de la version a partir de archivos
	print colored('We\'re trying to get the version through default files, please wait','green')
	m = hashlib.md5()
	elements = []
	
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href'] # Busqueda de imagenes, favicon, hojas de estilo y js
	
	requests.packages.urllib3.disable_warnings()					
	
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				res = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
		else:
			try:
				res = requests.get(arg, cookies = cookies, headers = headers, verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
	else:
		try:
			res = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
		except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
		
	webpage = html.fromstring(res.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)): # Busqueda de css, js, imagenes, favicon
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				if link.startswith('http'):	
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							try:
								req = requests.get(link,cookies = cookies, headers = headers,verify=False,timeout=10)
							except:
								print 'It seems that we have problems using Tor :(, you could try with proxy option instead of'
								sys.exit(2)
						else:
							try:
								req = requests.get(link, cookies = cookies, headers = headers, verify=False,timeout=10)
							except requests.exceptions.TimeoutError:
								print colored('Too many time waiting for Tor response, please try again','green')
								sys.exit(2)
					else:
						try:
							req = requests.get(link,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for Tor response, please try again','green')
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
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
		else:
			try:
				readme = requests.get(arg + '/README.txt', cookies = cookies, headers = headers, verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
	else:
		try:
			readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
		except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
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
		l.append('\nVersion getting from configuration files: ' + v)
		files(arg,verbose,v,cookies,headers,proxy,proxies,tor,report,l) # Obtencion de plugins y temas
		f.close()
		
		

def files(arg, verbose,version,cookies,headers,proxy,proxies,tor,report,l): # Obtencion de plugins y temas
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	for row in reader:
		try:
			if int(verbose) == 3: # Busqueda de archivos de configuracion visibles
				if 'Readme' in row[1] and 'Moodle' in row[0]: 
					readme = arg + row[2]
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							try:
								req = requests.get(readme,cookies = cookies, headers = headers,verify=False,timeout=10)
							except requests.exceptions.TimeoutError:
								print colored('Too many time waiting for Tor response, please try again','green')
								sys.exit(2)
						else:
							try:
								req = requests.get(readme, cookies = cookies, headers = headers, verify=False,timeout=10)
							except requests.exceptions.TimeoutError:
								print colored('Too many time waiting for Tor response, please try again','green')
								sys.exit(2)
					else:
						try:
							req = requests.get(readme,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for Tor response, please try again','green')
							sys.exit(2)
				
					if req.status_code == 200:
						print 'README file: ' + colored(readme, 'green')
						l.append('README file: ' + readme)
					elif req.status_code == 403:
						print 'Forbidden README: ' + colored(readme, 'green')
						l.append('Forbidden README: ' + readme)
					else:
						continue
		
				elif 'Change' in row[1] and 'Moodle' in row[0]: # Busqueda de archivos de configuracion visibles
					changeLog = arg +  row[2]
				
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							try:
								req = requests.get(changeLog,cookies = cookies, headers = headers,verify=False,timeout=10)
							except requests.exceptions.TimeoutError:
								print colored('Too many time waiting for Tor response, please try again','green')
								sys.exit(2)
						else:
							try:
								req = requests.get(changeLog, cookies = cookies, headers = headers, verify=False,timeout=10)
							except requests.exceptions.TimeoutError:
								print colored('Too many time waiting for Tor response, please try again','green')
								sys.exit(2)
					else:
						try:
							req = requests.get(changeLog,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for Tor response, please try again','green')
							sys.exit(2)
				
					if req.status_code == 200:
						print 'ChangeLog: ' + colored(changeLog,'green')
						l.append('ChangeLog: ' + changeLog)
					elif req.status_code == 403:
						print 'Forbidden ChangeLog: ' + colored(changeLog,'green')
						l.append('Forbidden ChangeLog: ' + changeLog)
					else:
						continue
			else:
				pass
				
			if 'Plugin' in row[1] and 'Moodle' in row[0]: # Busqueda de los plugins
				plugin = arg + row[2]
				if len(proxy) == 1:
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						try:
							req = requests.get(plugin,cookies = cookies, headers = headers,verify=False,timeout=10)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for Tor response, please try again','green')
							sys.exit(2)
					else:
						try:
							req = requests.get(plugin, cookies = cookies, headers = headers, verify=False,timeout=10)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for Tor response, please try again','green')
							sys.exit(2)
				else:
					try:
						req = requests.get(plugin,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for Tor response, please try again','green')
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
										l.append( "Plugin Name: " + begin)
									elif int(verbose) == 2:
										print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path,'green')
										l.append( "Plugin Name: " + begin + ', Path: ' + path)
									elif int(verbose) == 3:
										print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path, 'green') + ' ,Version: ' + colored(match.group(2),'blue')
										l.append( "Plugin Name: " + begin + ', Path: ' + path + ' ,Version: ' + match.group(2))
							except:
								if int(verbose) == 1:
									print "Plugin Name: " + colored(begin, 'green')
									l.append( "Plugin Name: " + begin)
								elif int(verbose) == 2 or int(verbose) == 3:
									print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path, 'green')
									l.append("Plugin Name: " + begin + ', Path: ' + path)
					except:
						continue
		
				elif req.status_code == 403:
					path = re.sub(r'upgrade.txt','',plugin)
					one = re.sub(r'^\/','',element)
					plug = re.sub(r'/upgrade.txt','',one)
					if int(verbose) == 3:
						print "Forbidden Plugin,  Name: " + colored(plug, 'yellow') + ', Path: ' + colored(path, 'green')
						l.append("Forbidden Plugin,  Name: " + plug + ', Path: ' + path)
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
			try:
				res = requests.get(arg,cookies = cookies, headers = headers,verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
		else:
			try:
				res = requests.get(arg, cookies = cookies, headers = headers, verify=False,timeout=10)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
				sys.exit(2)
	else:
		try:
			res = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False,timeout=10)
		except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for Tor response, please try again','green')
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
						l.append("Theme Name: " + match.group(3))
					elif int(verbose) == 2 or int(verbose) == 3:
						print "Theme Name: " + colored(match.group(3), 'green') + ', Path: ' + colored(element, 'green')
						l.append("Theme Name: " + match.group(3) + ', Path: ' + element)
			except:
				pass
		else:
			regex = re.compile(r'(.*)\/(.*)\/theme\/(.*)')
			match = regex.search(element)
			try:
				if match.group():
					if int(verbose) == 1:
						print "Theme Name: " + colored(match.group(2),'green')
						l.append( "Theme Name: " + match.group(2))
					elif int(verbose) == 2 or int(verbose) == 3:
						print "Theme Name: " + colored(match.group(2), 'green') + ', Path: ' + colored(match.group(1) + '/' + match.group(2), 'green')
						l.append("Theme Name: " + match.group(2) + ', Path: ' + match.group(1) + '/' + match.group(2))
			except:
				if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
					print "Theme Name: " + colored(match.group(2), 'green')
					l.append("Theme Name: " + match.group(2))
	
	vuln(version,verbose,report,l)
	sys.exit
		
def vuln(version,verbose,report,l): # Listado de vulnerabilidades obtenidas a partir de la version del gestor de contenidos
	f = open('vuln','rb')
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		try:
			if 'Moodle' in row[0] and row[1] in version:
				if int(verbose) == 1:
					print "Vulnerability Link: " + colored(row[3],'green')
					l.append( "Vulnerability Link: " + row[3])
				elif int(verbose) == 2 or int(verbose) == 3:
					l.append("Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + row[3])
					print "Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + colored(row[3],'green')
	
		except IndexError:
			sys.exit(2)
	f.close()
	rep(report,l)
	
def rep(list1,list2):
	for value in list1:
		if list1.index(value) == 0:
			t = time.strftime('%d-%m-%Y')
			h = time.strftime('%H:%M:%S')
			fo = open(('MoodleReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write('Results from the site\n')
			for element in list2:
				fo.write(element + '\n')
			fo.close()
		else:
			pass
