#!/usr/bin/python
import re
import requests
import sys
import argparse
from lxml import etree
from lxml import html
from termcolor import colored

arg = sys.argv[1]
visited = []
toVisit = []


def crawler(arg):
	print colored('Consulta del sitio: ','white') + colored(arg, 'green')
	if 'http://' in arg or 'https://' in arg: # Valida si tiene http(s)
		# Lista para encontrar elementos
		listFind = [ '//a/@href',  '//script/@src']
		
		# Peticiones
		try:
			requests.packages.urllib3.disable_warnings()					
			res = requests.post(arg, verify=False)
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
				if site in link: # Para los enlaces que contienen el nombre de dominio
					regex = re.compile(r'(.*)\.js') #Si el enlace contiene js se agrega a una lista que no se consulta
					js = regex.search(link)
					try:
						if js.group() not in visited:
							print colored('Link: ', 'white') + colored(js.group(),'blue')
							visited.append(link)
					except:
						regex = re.compile(r'(.*)\?(.*)') # Quita las variables despues de ?
						match = regex.search(link)
						try:
							if match.group():
								if match.group(1) not in toVisit and match.group(1) not in visited:
									print colored('Link: ', 'white') + colored(match.group(1),'blue')
									toVisit.append(match.group(1))
						except:
							if link not in toVisit and link not in visited: #Si el enlace no tiene variables
								print colored('Link: ', 'white') + colored(link,'blue')
								toVisit.append(link)
					
				else: #Otros enlaces Ej:'/'
					regex = re.compile(r'^\/(.*)') # Agrega los que tienen solo diagonal
					diagonal = regex.search(link)
					try:
						if diagonal.group():
							complete =  arg + link
							r = requests.head(complete)
							regex = re.compile(r'20[0-6]')
							status = regex.search(str(r.status_code))
							try:
								if status.group():
									if complete not in toVisit and complete not in visited:
										print colored('Link: ', 'white') + colored(complete,'blue')
										toVisit.append(complete)
							except:
								continue
					except:
						continue
			
			i + 1	
		
		
	else: # Si no tiene http
			http =  re.sub(r'(^)','http://',arg)
			crawler(http)
			exit(2)
	
	for element in range(0,5):
		visited.append(toVisit[element])
		toVisit.pop(element)
		
		crawler(toVisit[element])
	
	

crawler(arg)

