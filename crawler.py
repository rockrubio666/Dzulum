import re # Utilizado para regex
import requests # Utilizado para realizar las peticiones
import sys
import time
from lxml import etree # Utilizado para la obtencion de enlaces y js
from lxml import html # Utilizado para la obtencion de enlaces y js
from termcolor import colored
import socket # Tor
import socks # Tor
import random
import time


visited = []
toVisit = []

start_time = time.time()
def crawler(arg,verbose,cookie,agent,proxip,proxport,tor,report,th):
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	l = []
	j = []
	requests.packages.urllib3.disable_warnings()
	if len(proxy) == 1:
		if tor == True: # Peticiones a traves de tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				req = requests.get(arg,verify=False)
			except:
				sys.exit(2)
		else:
			req = requests.get(arg,verify=False)
	else: # Peticiones a traves de proxy
		try:
			req = requests.get(arg,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
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
	
	print colored("Beginning Crawling", 'blue')
	print 'Querying the site: ' + colored(arg, 'green')
	if 'http://' in arg or 'https://' in arg: # Valida si tiene http(s)
		# Lista para encontrar elementos
		listFind = [ '//a/@href',  '//script/@src'] # Busqueda de enlaces y js
		
		# Peticiones
		try:
			requests.packages.urllib3.disable_warnings()					
			if len(proxy) == 1:
				if tor == True:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket					
					res = requests.get(arg,cookies = cookies, headers = headers,verify=False)
				else:
					res = requests.get(arg, cookies = cookies, headers = headers, verify=False)
			else:
				req = requests.get(arg,cookies = cookies, headers = headers,proxies = proxies,verify=False)
			
			page_source = res.text
			webpage = html.fromstring(res.content)
			
		except:
			print "Error, site can't query"
			sys.exit(2)
			
		
		# Extrae los elementos de la pagina principal
		i = 0
		site =  re.sub(r'(http|https)://','',arg)
		
		for i in range(0,len(listFind)): # Obtiene los enlaces y js
			for link in webpage.xpath(listFind[i]):
				if site in link: # Para los enlaces que contienen el nombre de dominio
					regex = re.compile(r'(.*)\.js') #Si el enlace contiene js se agrega a una lista que no se consulta
					js = regex.search(link)
					try:
						if js.group() not in visited:
							if int(verbose) == 2 or int(verbose) == 3:
								print 'Link: ' + colored(js.group(),'blue')
								j.apped(js.group())
								#l.append('Link: ' + js.group())
							visited.append(link)
					except:
						regex = re.compile(r'(.*)\?(.*)') # Quita las variables despues de ?
						match = regex.search(link)
						try:
							if match.group():
								if match.group(1) not in toVisit and match.group(1) not in visited:
									print 'Link: ' + colored(match.group(1),'blue')
									l.append(match.group(1))
									toVisit.append(match.group(1))
						except:
							if link not in toVisit and link not in visited: #Si el enlace no tiene variables
								print 'Link: ' + colored(link,'blue')
								l.append(link)
								toVisit.append(link)
					
				else: #Otros enlaces Ej:'/'
					regex = re.compile(r'^\/(.*)') # Agrega los que tienen solo diagonal
					diagonal = regex.search(link)
					try:
						if diagonal.group():
							complete =  arg + link
							if len(proxip) == 0:
								r = requests.head(complete, cookies = cookies, headers = headers, verify=False)
							else:
								proxy = proxip  + ':' + proxport
								proxies = {'http' : proxy, 'https' : proxy,}
								r = requests.head(complete,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
							
							
							regex = re.compile(r'20[0-6]')
							status = regex.search(str(r.status_code))
							try:
								if status.group(): # Si el codigo de estado es 200, lo agrega a una lista para una posterior consulta
									if complete not in toVisit and complete not in visited:
										print 'Link: ' + colored(complete,'blue')
										l.append(complete)
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
	rep(report,l,j,arg)
	#for element in range(len(toVisit)):
	#	visited.append(toVisit[element])
	#	print colored(toVisit[element], 'blue')
		#toVisit.pop(element)
		
		#crawler(toVisit[element])
	
	
def rep(rep,sites,js,arg):
	title = ' *** Results of Crawling***'
	execution =  ('Execution time was: %s seconds' % (time.time() - start_time))
	resource = 'Resource: ' + str(arg)
	f = 'Total of links found: ' + str(len(sites) + len(js))
	t = time.strftime('%d-%m-%Y')
	h = time.strftime('%H:%M:%S')
	
	for value in rep:
		if 'text' in value:
			fo = open(('CrawlerReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write(title.center(100) + '\n')
			fo.write('' + '\n')
			fo.write(execution.ljust(50) + '\n')
			fo.write('' + '\n')
			fo.write(resource.ljust(50) + '\n')
			fo.write(f.ljust(50) + '\n')
			fo.write('' + '\n')
			
			if len(js) == 0:
				pass
			else:
				fo.write('JavaScript Files'.center(100) + '\n')
				fo.write('' + '\n')
				for element in js:
					fo.write(element + '\n')
			
			if len(sites) == 0:
				pass
			else:
				fo.write('Links founnd'.center(100) + '\n')
				fo.write('' + '\n')
				for element in sites:
					fo.write('Link: ' + element + '\n')
			
			fo.close()
			
		elif 'html'.upper() in value or 'html' in value:			
			fo = open(('CrawlerReport_' + t + '_'+ h + '.html'), 'wb')
			
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

				<title>Results of Crawling</title>
			</head>
			<body text = "B8860B"; link ="B8860B"; bgcolor="00008B">
				<h1 align="center">Results of Crawling</h1><br><br>
			"""
			fo.write( header)
			fo.write("""<h1 align="left"> %s </h1>""" % execution)
			fo.write("""<h1 align="left"><a href='%s'> %s </a></h1>""" % (arg,resource))
			fo.write("""<h1 align="left"> %s </h1><br>""" % f)
			
			if len(js) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> JavaScript Files </h1><br>""")
				fo.write("""<table>""")
				for element in js: 	
					fo.write("""<tr><th><a href='%s'> %s </a></th></tr>""" % (element,element))
				fo.write("""</table><br>""")
				
			if len(sites) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Links found </h1><br>""")				
				fo.write("""<table>""")
				for element in sites:
					fo.write("""<tr><th><a href='%s'> %s </a></th></tr>""" % (element,element))
				
			fo.write("""</table>
			</body>
			</html>""")
			fo.close()
		
		elif 'xml'.upper() in value or 'xml' in value:			
			fo = open(('CrawlerReport_' + t + '_'+ h + '.xml'), 'wb')
			
			header = """<?xml version="1.0" encoding="UTF-8"?>
			<crawling>
				
			"""
			fo.write( header)
			fo.write(""" <time>%s</time>""" % execution)
			fo.write(""" <resource>%s</resource>""" % resource)
			fo.write("""<total>%s</total>""" % f)
			
			if len(js) == 0:
				pass
			else:
				for element in js: 	
					fo.write("""<js> %s </js>""" % (element))
			if len(sites) == 0:
				pass
			else:
				for element in sites:
					fo.write("""<link> %s </link>""" % (element))
			fo.write("""</crawling> """)
			fo.close()
		else:
			pass

