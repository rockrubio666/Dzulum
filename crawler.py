#!/usr/bin/python
# Existe un error que no pude solucionar
import re
import requests
import sys
from lxml import etree
from lxml import html


arg = sys.argv[1]

def crawler(arg):
	
	if 'http://' in arg or 'https://' in arg: # Valida si tiene http(s)
		# Lista para encontrar elementos
		listFind = [ '//a/@href',  '//img/@src', '//script/@src', ('//head/link[@rel="stylesheet"]/@href')]
		listLinks = []
		
		# Peticiones
		res = requests.post(arg)
		page_source = res.text
		webpage = html.fromstring(res.content)

	# Extrae los elementos de la pagina principal
		i = 0
		for i in range(0,len(listFind)):
			for link in webpage.xpath(listFind[i]):
				if link not in listLinks and '/' in link:
					listLinks.append(link)
			i + 1	
		
		# De los elementos encontrados trae sus recursos
		element = 0
		i = 0
		for element in range(0,2):
			res = requests.post(listLinks[element])
			page_source = res.text
			webpage = html.fromstring(res.content)
			
			for i in range(0,len(listFind)):
				for link in webpage.xpath(listFind[i]):
					if link not in listLinks and '/' in link:
						listLinks.append(link)
					
				i + 1
			element + 1
		
	
	else: # Si no tiene http
		http =  re.sub(r'(^)','http://',arg)
		crawler(http)
		exit(2)

	print "Total de enlaces"
	for l in range(len(listLinks)):
			print listLinks[l]	
	
crawler(arg)


