import urllib2
import re

response = urllib2.urlopen('https://tuaulavirtual.educatic.unam.mx/')
page_source = response.read()
fo = open('ejemplo.text','w')
fo.write(page_source)
fo.close()

fo = open('ejemplo.text','r')
for line in fo:
	matchObj = re.match(r'(.*) (src|href)=("(.*)")(.*)>', line)
	if matchObj:
		print matchObj.group() + "\n"
fo.close()
