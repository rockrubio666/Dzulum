
import requests
import socket
import sys
import getopt

ip = ''
site = ''
arg = ''

def help():
	print('-p, --ip Direccion IP del sitio \n'
		  '-s, --site Direccion URL del sitio\n'
		  '-h, ---help Ayuda\n')


def validateIP(ip):
	try:
		test = ip.split('/')
		socket.inet_aton(test[0])
		site = socket.gethostbyaddr(test[0])
		print "Direccion IP del sitio: " + test[0]
		print "Direccion URL del sitio: " + site[0]
	except socket.error:
		print "ip no valida"
		
def validateSite(site):
	try:
		test = site.split('/')
		print "Direccion IP del sitio: " + socket.gethostbyname(test[0])
		print "Direccion URL del sitio: " + site		
	except:
		print 'sitio no valido'
	
	
def getParams(arg):
	try:
		opts, args = getopt.getopt(sys.argv[1:],'i:s:h', ['ip=', 'site=','help'])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:	
		if opt in ('-i','--ip'):
			ip = arg
			validateIP(ip)
	
		elif opt in ('-s', '--site'):
			site = arg
			validateSite(site)
		
		elif opt in ('-h','--help'):
			h = arg
					
		else:
			print 'opcion no valida'
			sys.exit(2)


getParams(arg)
