#!/usr/bin/python
import re
import requests
import sys
from lxml import etree
from lxml import html


arg = sys.argv[1]

def crawler(arg):
	
	if 'http://' in arg or 'https://' in arg: # Valida si tiene http(s)
		# Lista para encontrar elementos
		listFind = [ '//a/@href',  '//script/@src','//link[@rel="short icon"]/@href']
		listLinks = []
		
		# Peticiones
		try:
			res = requests.post(arg)
			page_source = res.text
			webpage = html.fromstring(res.content)
			
		except:
			print "Error, no se pudo consultar el sitio"
			sys.exit(2)
		
		# Extrae los elementos de la pagina principal
		i = 0
		site =  re.sub(r'(http|https)://','',arg)
		
		
		for i in range(0,len(listFind)):
			for link in webpage.xpath(listFind[i]):
				if site in link: # Valida que sea del dominio que se pasa como argumento
					regex = re.compile(r'(.*)\?(.*)') # Quita las variables despues de ?
					match = regex.search(link)
					try:
						if match.group():
							if match.group(1) not in listLinks:
								listLinks.append(match.group(1))
					except:
						if link not in listLinks:
							listLinks.append(link)
				else:
					regex = re.compile(r'^\/(.*)')
					match = regex.search(link)
					try:
						if match.group():
							complete =  arg + link
							if complete not in listLinks:
								listLinks.append(complete)
					except:
						continue
			i + 1	
		
		
	else: # Si no tiene http
			http =  re.sub(r'(^)','http://',arg)
			crawler(http)
			exit(2)
	
	#Archivos con extension .php,.js
	for element in listLinks:
		regex = re.compile(r'(.*)(\..*$)')
		match = regex.search(element)
		try:
			if match.group():
				if match.group() not in listLinks:
					listLinks.append(match.group())
		except:
			continue
	
	
	print "Total de enlaces:"
	for l in range(len(listLinks)):
		print listLinks[l]	
	sys.exit(2)
	
		
crawler(arg)


