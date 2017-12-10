#!/usr/bin/python

import socket
import re
import sys
import requests
import hashlib
from lxml import etree
from lxml import html
import wget
import os
from collections import Counter
import operator
from termcolor import colored
import csv


plugins = ['']

def moodle(arg, verbose,cookie,agent,proxip,proxport):
# Si el argumento tiene http(s)
	requests.packages.urllib3.disable_warnings()
	if len(proxip) == 0:
		req = requests.get(arg,verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		req = requests.get(arg,proxies = {'http':proxy},verify=False)
	
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

	m = hashlib.md5()
	
	if 'http://' in arg or 'https://' in arg:
		requests.packages.urllib3.disable_warnings()
	
		headers = {'user-agent': agent}
		cookies = dict(cookies_are=cookie) 
		if len(proxip) == 0:
			upgrade = requests.get(arg + '/lib/upgrade.txt', cookies = cookies, headers = headers,verify=False)
		else:
			proxy = proxip  + ':' + proxport
			proxies = {'http' : proxy, 'https' : proxy,}
			upgrade = requests.get(arg + '/lib/upgrade.txt',cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
						
		if int(upgrade.status_code) == 200: #Si tiene el archivp upgrade
			regex = re.compile(r'===(.*)===')
			match = regex.search(upgrade.text)
			try:
				if match.group(): #Si es un numero de version
					if int(verbose) == 1:
						print 'Version del sitio: ' + colored(match.group(1),'green')
					elif int(verbose) == 2:
						print "La version del sitio: " + colored(arg,'green') + " es: " + colored(match.group(1),'green')
					elif int(verbose) == 3:
						print "Version del sitio encontrada en: " + colored(upgrade.url,'green')
					files(arg,verbose,match.group(1),cookie,agent,proxip,proxport)
				
					
			except:
				exit(2)
		
		else: #Si no lo tiene
			version(arg,verbose,cookie,agent,proxip,proxport)
			
			
# Si no tiene http(s) se pega a la direccion
	else:
		http =  re.sub(r'(^)','http://',arg)
		moodle(http)
		exit(2)
		

def version(arg,verbose,cookie,agent,proxip,proxport):	
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href']
	
	requests.packages.urllib3.disable_warnings()					
	
	headers = {'user-agent': agent}
	cookies = dict(cookies_are=cookie) 
	
	if len(proxip) == 0:
		res = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		res = requests.get(arg,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
		
	webpage = html.fromstring(res.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)):
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				if link.startswith('http'):	
					headers = {'user-agent': agent}
					cookies = dict(cookies_are=cookie) 
					if len(proxip) == 0:
						req = requests.get(link, cookies = cookies, headers = headers, verify=False)
					else:
						proxy = proxip  + ':' + proxport
						proxies = {'http' : proxy, 'https' : proxy,}
						req = requests.get(link,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
						
					if req.status_code == 200 and i in range(2,3):
						try:
							filename = wget.download(link, bar=None)
							m.update(filename)
							hs = m.hexdigest()
							elements.append(hs)
							os.remove(filename)
						except:
							continue
				
					else:
						try:
							m.update(req.text)
							hs =  m.hexdigest()
							elements.append(hs)
						except:
							continue
	headers = {'user-agent': agent}
	cookies = dict(cookies_are=cookie) 			
	if len(proxip) == 0:
		readme = requests.get(arg + '/README.txt', cookies = cookies, headers = headers, verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		readme = requests.get(arg + '/README.txt',cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
	if readme.status_code == 200:
		try:
			m.update(readme.text)
			hs = m.hexdigest()
			elements.append(hs)
		except:
			pass
		
	
	
	f = open('versions','rb')		
	reader = csv.reader(f,delimiter=',')
			
	for element in elements:
		for row in reader:
			try:
				if element in row[2] and 'Moodle' in row[0]:
					average.append(row[1])
			except:
				continue
	
	cnt = Counter(average)
	if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
		v = max(cnt.iteritems(),key=operator.itemgetter(1))[0]
		print '\nVersion del sitio aproximada mediante archivos de configuracion: ' + colored(v, 'green')
	files(arg,verbose,v,proxip,proxport)
	f.close()

def files(arg, verbose,version,cookie,agent,proxip,proxport):
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	for row in reader:
		try:
			if 'Readme' in row[1] and 'Moodle' in row[0]: 
				readme = arg + row[2]
				headers = {'user-agent': agent}
				cookies = dict(cookies_are=cookie) 
				if len(proxip) == 0:
					req = requests.get(readme, cookies = cookies, headers = headers, verify=False)
				else:
					proxy = proxip  + ':' + proxport
					proxies = {'http' : proxy, 'https' : proxy,}
					req = requests.get(readme,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
				
				if req.status_code == 200 and int(verbose) == 3:
					print 'README file: ' + colored(readme, 'green')
				elif req.status_code == 403 and int(verbose) == 3:
					print 'Forbidden README: ' + colored(readme, 'green')
				else:
					continue
		
			elif 'Change' in row[1] and 'Moodle' in row[0]:
				changeLog = arg +  row[2]
				
				headers = {'user-agent': agent}
				cookies = dict(cookies_are=cookie) 
				if len(proxip) == 0:
					req = requests.get(changeLog, cookies = cookies, headers = headers, verify=False)
				else:
					proxy = proxip  + ':' + proxport
					proxies = {'http' : proxy, 'https' : proxy,}
					req = requests.get(changeLog,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
				
				if req.status_code == 200 and int(verbose) == 3:
					print 'ChangeLog: ' + colored(changeLog,'green')
				elif req.status_code == 403 and int (verbose) == 3:
					print 'Forbidden ChangeLog: ' + colored(changeLog,'green')
				else:
					continue
			
			elif 'Plugin' in row[1] and 'Moodle' in row[0]:
				plugin = arg + row[2]
				headers = {'user-agent': agent}
				cookies = dict(cookies_are=cookie) 
				if len(proxip) == 0:
					req = requests.get(plugin, cookies = cookies, headers = headers, verify=False)
				else:
					proxy = proxip  + ':' + proxport
					proxies = {'http' : proxy, 'https' : proxy,}
					req = requests.get(plugin,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
				
				if req.status_code == 200:
					up = re.sub(r'\/upgrade.txt','',row[2])
					begin = re.sub(r'^\/','',up)
					regex = re.compile(r'(===)(.*)(===)')
					match = regex.search(req.text)
					try:
						if match.group():
							path = re.sub(r'upgrade.txt','',plugin)
						try:
							if complex(match.group(2)):
								if int(verbose) == 1:
									print "Plugin Name: " + colored(begin, 'green')
								elif int(verbose) == 2:
									print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path,'green')
								elif int(verbose) == 3:
									print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path, 'green') + ' ,Version: ' + colored(match.group(2),'blue')
						except:
							if int(verbose) == 1:
								print "Plugin Name: " + colored(begin, 'green')
							elif int(verbose) == 2 or int(verbose) == 3:
								print "Plugin Name: " + colored(begin, 'green') + ', Path: ' + colored(path, 'green')
					except:
						continue
		
				elif req.status_code == 403:
					path = re.sub(r'upgrade.txt','',plugin)
					one = re.sub(r'^\/','',element)
					plug = re.sub(r'/upgrade.txt','',one)
					if int(verbose) == 3:
						print "Forbidden Plugin,  Name: " + colored(plug, 'yellow') + ', Path: ' + colored(path, 'green')
						continue
					else:
						continue

		except:
			continue	
	f.close()		
	
	headers = {'user-agent': agent}
	cookies = dict(cookies_are=cookie) 
	if len(proxip) == 0:
		res = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		proxy = proxip  + ':' + proxport
		proxies = {'http' : proxy, 'https' : proxy,}
		res = requests.get(arg,cookies = cookies, headers = headers,proxies = {'http':proxy},verify=False)
	
	webpage = html.fromstring(res.text)
	theme =  webpage.xpath('//link[@rel="shortcut icon"]/@href')
	
	for element in theme:
		if '=' in element:
			regex = re.compile(r'(.*)(theme=)(.*)(\&image=(.*))')
			match = regex.search(element)
			try:
				if match.group():
					if int(verbose) == 1:
						print "Theme Name: " + colored(match.group(3), 'green')
					elif int(verbose) == 2 or int(verbose) == 3:
						print "Theme Name: " + colored(match.group(3), 'green') + ', Path: ' + colored(element, 'green')
			except:
				pass
		else:
			regex = re.compile(r'(.*)\/(.*)\/theme\/(.*)')
			match = regex.search(element)
			try:
				if match.group():
					if int(verbose) == 1:
						print "Theme Name: " + colored(match.group(2),'green')
					elif int(verbose) == 2 or int(verbose) == 3:
						print "Theme Name: " + colored(match.group(2), 'green') + ', Path: ' + colored(match.group(1) + '/' + match.group(2), 'green')
			except:
				if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
					print "Theme Name: " + colored(match.group(2), 'green')
	vuln(version,verbose)
	sys.exit
		
def vuln(version,verbose):
	f = open('vuln','rb')
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		if 'Moodle' in row[0] and row[1] in version:
			if int(verbose) == 1:
				print "Vulnerability Link: " + colored(row[3],'green')
			elif int(verbose) == 2 or int(verbose) == 3:
				print "Vulnerability Name: " + colored(row[2],'green') + ' ,Vulnerability Link: ' + colored(row[3],'green')
	f.close()
	
