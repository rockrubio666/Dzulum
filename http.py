import requests
import getopt
import sys

arg = ''

def http(arg):
	proxies = {'http:' : arg,
				'https:' : arg}
			
	r = requests.get('http://httpbin.org/ip', proxies=proxies)
	print r.text
	print r


def getParams(arg):
	try:
		opts, args = getopt.getopt(sys.argv[1:],'p:h', ['http=''help'])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:	
		if opt in ('-p','--http'):
			ht = arg
			http(ht)
	
		
		elif opt in ('-h','--help'):
			print "prueba"
					
		else:
			print 'opcion no valida'
			sys.exit(2)

getParams(arg)





