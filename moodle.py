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

plugins = ['']

def moodle(arg, verbose,cookie,agent,proxip,proxport,tor,report): # Version
# Si el argumento tiene http(s)
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	l = []
	requests.packages.urllib3.disable_warnings()
	
	if len(proxy) == 1:
		if tor == True: # Peticiones a traves de Tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			req = requests.get(arg,verify=False)
		else:
			req = requests.get(arg,verify=False)
	else: # Peticiones a traves del proxy
		try:
			req = requests.post(arg,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print 'There\'s a problem with the proxy connection, please check it and try again :D '
			sys.exit(2)
	
	if cookie is None: # Obtencion de la cookie de sesion
		for key,value in req.headers.iteritems():
			if 'set-cookie' in key:
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

	m = hashlib.md5()
	
	if 'http://' in arg or 'https://' in arg:
		requests.packages.urllib3.disable_warnings()
	
		headers = {'user-agent': agent}
		cookies = {'': cookie}
		if len(proxy) == 1:
			if tor == True:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
				socket.socket = socks.socksocket
				upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,verify=False)
			else:
				upgrade = requests.get(arg + '/lib/upgrade.txt', cookies = cookies, headers = headers,verify=False)
		else:

			upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,proxies = proxies,verify=False)
						
		if int(upgrade.status_code) == 200: #Si tiene el archivo upgrade
			regex = re.compile(r'===(.*)===')
			match = regex.search(upgrade.text)
			try:
				if match.group(): #Si es un numero de version
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
					files(arg,verbose,match.group(1),cookie,agent,proxy,proxies,tor,report,l) # Si existe el archivo se obtienen los plugins y el tema
				
					
			except:
				exit(2)
		
		else: #Si no lo tiene
			version(arg,verbose,cookie,agent,proxy,proxies,tor,report,l) # Si no se obtiene la version a partir del archivo, se obtiene a partir de los archivos por defecto
			
			
# Si no tiene http(s) se pega a la direccion
	else:
		http =  re.sub(r'(^)','http://',arg)
		moodle(http)
		exit(2)
		

def version(arg,verbose,cookie,agent,proxy,proxies,tor,report,l):	 # Obtencion de la version a partir de archivos
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href'] # Busqueda de imagenes, favicon, hojas de estilo y js
	
	requests.packages.urllib3.disable_warnings()					
	
	headers = {'user-agent': agent}
	cookies = {'': cookie} 
	
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			res = requests.get(arg,cookies = cookies, headers = headers,verify=False)
		else:
			res = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		res = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False)
		
	webpage = html.fromstring(res.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)): # Busqueda de css, js, imagenes, favicon
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				if link.startswith('http'):	
					headers = {'user-agent': agent}
					cookies = {'': cookie} 
					if len(proxy) == 1:
						if tor == True:
							socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
							socket.socket = socks.socksocket
							try:
								req = requests.get(link,cookies = cookies, headers = headers,verify=False)
							except:
								print 'It seems that we have problems using Tor :(, you could try with proxy option instead of'
								sys.exit(2)
						else:
							req = requests.get(link, cookies = cookies, headers = headers, verify=False)
					else:
						req = requests.get(link,cookies = cookies, headers = headers,proxies = proxies,verify=False)
						
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
	headers = {'user-agent': agent}
	cookies = {'': cookie} 			
	if len(proxy) == 1: # Obtencion del hash del archivo README
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,verify=False)
		else:
			readme = requests.get(arg + '/README.txt', cookies = cookies, headers = headers, verify=False)
	else:
		readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,proxies = proxies,verify=False)
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
		v = max(cnt.iteritems(),key=operator.itemgetter(1))[0]
		print '\nVersion getting from configuration files: ' + colored(v, 'green')
		l.append('\nVersion getting from configuration files: ' + v)
	files(arg,verbose,v,proxy,proxies,tor,report,l) # Obtencion de plugins y temas
	f.close()

def files(arg, verbose,version,cookie,agent,proxy,proxies,tor,report,l): # Obtencion de plugins y temas
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	for row in reader:
		try:
			if int(verbose) == 3: # Busqueda de archivos de configuracion visibles
				if 'Readme' in row[1] and 'Moodle' in row[0]: 
					readme = arg + row[2]
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
					elif req.status_code == 403:
						print 'Forbidden README: ' + colored(readme, 'green')
						l.append('Forbidden README: ' + readme)
					else:
						continue
		
				elif 'Change' in row[1] and 'Moodle' in row[0]: # Busqueda de archivos de configuracion visibles
					changeLog = arg +  row[2]
				
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
					elif req.status_code == 403:
						print 'Forbidden ChangeLog: ' + colored(changeLog,'green')
						l.append('Forbidden ChangeLog: ' + changeLog)
					else:
						continue
			else:
				pass
				
			if 'Plugin' in row[1] and 'Moodle' in row[0]: # Busqueda de los plugins
				plugin = arg + row[2]
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
				
				if req.status_code == 200: # Obtencion de la version del plugin
					up = re.sub(r'\/upgrade.txt','',row[2])
					begin = re.sub(r'^\/','',up)
					regex = re.compile(r'(===)(.*)(===)')
					match = regex.search(req.text)
					try:
						if match.group():
							path = re.sub(r'upgrade.txt','',plugin)
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
	
	headers = {'user-agent': agent}
	cookies = {'': cookie} 
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			res = requests.get(arg,cookies = cookies, headers = headers,verify=False)
		else:
			res = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		res = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False)
	
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
		if 'Moodle' in row[0] and row[1] in version:
			if int(verbose) == 1:
				print "Vulnerability Link: " + colored(row[3],'green')
				l.append( "Vulnerability Link: " + row[3])
			elif int(verbose) == 2 or int(verbose) == 3:
				l.append("Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + row[3])
				print "Vulnerability Name: " + row[2] + ' ,Vulnerability Link: ' + colored(row[3],'green')
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


