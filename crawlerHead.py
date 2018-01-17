import requests # Utilizado para hacer las peticiones
import re # Utilizado para regex
import sys
import os
import time
from lxml.html import fromstring # Utilizado para exztraer los enlaces
from termcolor import colored
import socket # Tor
import socks # Tor
import random
import time	

start_time = time.time()
def crawlerHead(url,f,verbose,cookie,agent, proxip,proxport,tor,report,th):
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
		
	
	c = []
	d = []
	t = []
	i = []
	requests.packages.urllib3.disable_warnings()
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050) # Peticiones a traves de tor
			socket.socket = socks.socksocket
			try:
				req = requests.get(url,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			
		else:
			try:
				req = requests.get(url,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
	else: # Peticiones a traves del proxy
		try:
			req = requests.get(url,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print colored('It can\'t contact with the page','green')
			sys.exit(2)
		except requests.RequestException:
			print colored('It can\'t contact with the page','green')
			sys.exit(2)
		except requests.exceptions.Timeout:
			print colored('Too many time waiting for response, please try again','green')
			sys.exit(2)
		except:
			print colored('It can\'t contact with the page','green')
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
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				req = requests.head(resources[0],cookies = cookies, headers = headers,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
		else:
			try:
				req = requests.head(resources[0], cookies = cookies, headers = headers, verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
	else:
		try:
			req = requests.head(resources[0],cookies = cookies, headers = headers,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print colored('It can\'t contact with the page','green')
			sys.exit(2)
		except requests.RequestException:
			print colored('It can\'t contact with the page','green')
			sys.exit(2)
		except requests.exceptions.Timeout:
			print colored('Too many time waiting for response, please try again','green')
			sys.exit(2)
		except:
			print colored('It can\'t contact with the page','green')
			sys.exit(2)
			
	
	fake.append(req.url)
	for key,value in req.headers.iteritems():
		if 'location' in key:
			f = value
	
	
	resources.pop(0)
	print 'Looking for resources in: ' + colored(sites[0],'green')
	

	for element in resources: # Por cada elemento de la lista, se hace la peticion y se ve el codigo de estado
		
		other  = element.rstrip()
		requests.packages.urllib3.disable_warnings()					
		
		if len(proxy) == 1:
			if tor == True:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
				socket.socket = socks.socksocket
				try:
					res = requests.get(other,cookies = cookies, headers = headers,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the page','green')
					sys.exit(2)
				except requests.exceptions.Timeout:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
				except:
					print colored('It can\'t contact with the page','green')
					sys.exit(2)
			else:
				try:
					res = requests.head(other, cookies = cookies, headers = headers, verify=False)
					res.connection.close()
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the page','green')
					sys.exit(2)
				except requests.exceptions.Timeout:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
				except:
					print colored('It can\'t contact with the page','green')
					sys.exit(2)
			
		else:
			try:
				res = requests.head(other,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				res.connection.close()
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the page','green')
				sys.exit(2)
		
		regex = re.compile(r'20[0-6]')
		match = regex.search(str(res.status_code))
		try:
			if match.group():	# Si el codigo de estado es 200, se muestra el recurso
				if element not in sites:
					sites.append(element)
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print "Resource exists: " + colored(element, 'green') + " Status code: " + colored(res.status_code, 'yellow')
						d.append(element)
						d.append(res.status_code)
		
						
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
							if len(proxy) == 1:
								if tor == True:
									socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)	
									socket.socket = socks.socksocket
									try:
										r = requests.get(indexOf,cookies = cookies, headers = headers,verify=False)
									except requests.exceptions.ConnectionError:
										print colored('It can\'t contact with the page','green')
										sys.exit(2)
									except requests.RequestException:
										print colored('It can\'t contact with the page','green')
										sys.exit(2)
									except requests.exceptions.Timeout:
										print colored('Too many time waiting for response, please try again','green')
										sys.exit(2)
									except:
										print colored('It can\'t contact with the page','green')
										sys.exit(2)
								else:
									try:
										r = requests.get(indexOf,cookies=cookies,headers=headers,verify=False)
									except requests.exceptions.ConnectionError:
										print colored('It can\'t contact with the page','green')
										sys.exit(2)
									except requests.RequestException:
										print colored('It can\'t contact with the page','green')
										sys.exit(2)
									except requests.exceptions.Timeout:
										print colored('Too many time waiting for response, please try again','green')
										sys.exit(2)
									except:
										print colored('It can\'t contact with the page','green')
										sys.exit(2)
							else:
								try:
									r = requests.get(indexOf,cookies = cookies, headers = headers,proxies = proxies,verify=False)
								except requests.exceptions.ConnectionError:
									print colored('It can\'t contact with the page','green')
									sys.exit(2)
								except requests.RequestException:
									print colored('It can\'t contact with the page','green')
									sys.exit(2)
								except requests.exceptions.Timeout:
									print colored('Too many time waiting for response, please try again','green')
									sys.exit(2)
								except:
									print colored('It can\'t contact with the page','green')
									sys.exit(2)
								
							if r.status_code == 200 and '<title>Index of' in r.content: # Siel codigo de estado es 300, se verifica si muestra index of
								print "Index of: " + colored(r.url, 'green') + " Status code: " + colored(r.status_code, 'yellow')
								i.append(r.url)
								i.append(r.status_code)
								
							elif r.status_code == 200:
								print "Resource exists: " + colored(r.url, 'green') + " Status code: " + colored(r.status_code, 'yellow') # O si el codigo de estado es 200
								d.append(r.url)
								d.append(r.status_code)
								
							elif r.status_code == 403: # Si es un forbidden, se vuelve a pasar la lista de sitios
								if os.path.exists(f):
									fo = open(f, 'r')
									for line in fo:
										new = r.url + line
										if len(proxy) == 1:
											if tor == True:
												socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
												socket.socket = socks.socksocket
												try:
													rn = requests.head(new.rstrip('\n'),cookies = cookies, headers = headers,verify=False)
												except requests.exceptions.ConnectionError:
													print colored('It can\'t contact with the page','green')
													sys.exit(2)
												except requests.RequestException:
													print colored('It can\'t contact with the page','green')
													sys.exit(2)
												except requests.exceptions.Timeout:
													print colored('Too many time waiting for response, please try again','green')
													sys.exit(2)
												except:
													print colored('It can\'t contact with the page','green')
													sys.exit(2)
											else:
												try:
													rn = requests.head(new.rstrip('\n'),cookies=cookies,headers=headers,verify=False)
												except requests.exceptions.ConnectionError:
													print colored('It can\'t contact with the page','green')
													sys.exit(2)
												except requests.RequestException:
													print colored('It can\'t contact with the page','green')
													sys.exit(2)
												except requests.exceptions.Timeout:
													print colored('Too many time waiting for response, please try again','green')
													sys.exit(2)
												except:
													print colored('It can\'t contact with the page','green')
													sys.exit(2)
										else:
											try:
												rn = requests.head(new.strip('\n'),cookies = cookies, headers = headers,proxies = proxies,verify=False)
											except requests.exceptions.ConnectionError:
												print colored('It can\'t contact with the page','green')
												sys.exit(2)
											except requests.RequestException:
												print colored('It can\'t contact with the page','green')
												sys.exit(2)
											except requests.exceptions.Timeout:
												print colored('Too many time waiting for response, please try again','green')
												sys.exit(2)
											except:
												print colored('It can\'t contact with the page','green')
												sys.exit(2)
			
		
										if rn.status_code == 200:
											print "Resource exists: " + colored(rn.url, 'green') + " Status code: " + colored(rn.status_code, 'yellow')
											c.append(rn.url)
											c.append(rn.status_code)
									fo.close()
								else:
									print "File not found"
								
						for key, value in res.headers.iteritems():
							if 'location' in key: 
								if value in f:
									fake.append(res.url)	
						
			except:
				pass
	
	rep(report,d,i,url)
	
def rep(rep,dos,index,url):
	title = ' *** Results of Crawling***'
	execution =  ('Execution time was: %s seconds' % (time.time() - start_time))
	resource = 'Resource: ' + str(url)
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
			fo.write('' + '\n')
			
			if len(dos) == 0:
				pass
			else:
				fo.write('Paths found with status code 200'.center(100) + '\n')
				fo.write('' + '\n')
				while len(dos) > 0:
					fo.write(str(dos[0]) + '\n')
					dos.pop(1)
					dos.pop(0)
					
			if len(index) == 0:
				pass
			else:
				fo.write('Paths found with Index of'.center(100) + '\n')
				fo.write('' + '\n')
				while len(index) > 0:
					fo.write(str(index[0]) + '\n')
					index.pop(1)
					index.pop(0)
			
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

				<title>Bruteforce Results</title>
			</head>
			<body text = "B8860B"; link ="B8860B"; bgcolor="00008B">
				<h1 align="center">Results of Crawling</h1><br><br>
			"""
			fo.write(header)
			fo.write("""<h1 align="left"> %s </h1>""" % execution)
			fo.write("""<h1 align="left"><a href='%s'> %s </a></h1><br>""" % (url,resource))
			
			if len(dos) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Paths found with status code 200 </h1><br>""")
				fo.write("""<table>""")
				while len(dos) > 0:
					fo.write("""<tr>
									<th><a href='%s'> %s </a></th></tr>
								</tr>""" % (dos[0],dos[0]))
					dos.pop(1)
					dos.pop(0)
				fo.write("""</table><br>""")
				
			if len(index) == 0:
				pass
			else:
				fo.write("""<h1 align="center"> Paths found with Index of </h1><br>""")
				fo.write("""<table>""")
				while len(index) > 0:
					fo.write("""<tr>
									<th><a href='%s'> %s </a></th></tr>
								</tr>""" % (index[0],index[0]))
					index.pop(1)
					index.pop(0)
				fo.write("""</table><br>""")
						
			fo.write("""</body>
			</html>""")
			fo.close()
