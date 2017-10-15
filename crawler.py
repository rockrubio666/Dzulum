#!/usr/bin/python

import re
import requests
from lxml import etree
from lxml import html

arg = 'https://www.seguridad.unam.mx'
#arg = 'https://aula.cert.unam.mx'
#arg = 'https://tuaulavirtual.educatic.unam.mx/'
res = requests.post(arg)
page_source = res.text
webpage = html.fromstring(res.content)


print "imagenes"
for link in webpage.xpath('//img/@src'):
	print link
print "links"
for link in webpage.xpath('//a/@href'):
	print link
print "java"
for link in webpage.xpath('//script/@src'):
	print link
print "css"
links = webpage.xpath('//head/link[@rel="stylesheet"]')
hrefs = [l.attrib['href'] for l in links]
print hrefs

#####Falta: Organizarlo, recibir parametros, ingresar a cada sitio, separar los css
