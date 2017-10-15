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
		listFind = [ '//a/@href',  '//img/@src', '//script/@src', ('//head/link[@rel="stylesheet"]/@href')]
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
		for i in range(0,len(listFind)):
			for link in webpage.xpath(listFind[i]):
				if link not in listLinks and '/' in link:
					listLinks.append(link)
			i + 1	
		
			# De los elementos encontrados trae sus recursos
		try:
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
		except:
			print "Total de enlaces:"
			for l in range(len(listLinks)):
				print listLinks[l]	
			print "Error en algun enlace del subsitio"
			sys.exit(2)
		
		
			
	else: # Si no tiene http
			http =  re.sub(r'(^)','http://',arg)
			crawler(http)
			exit(2)

	print "Total de enlaces:"
	for l in range(len(listLinks)):
		print listLinks[l]	
	sys.exit(2)
					
		
crawler(arg)


