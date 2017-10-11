import requests
import socket
import sys
import getopt

try:
	opts, args = getopt.getopt(sys.argv[1:],'i:s:h', ['ip=', 'site=','help'])
except getopt.GetoptError:
	print 'opcion no valida'
	print '-p, --ip Direccion IP del sitio'
	print '-s, --site Direccion URL del sitio'

	sys.exit(2)

for opt, arg in opts:
	
	if opt in ('-i','--ip'):
		line = arg
		try:
			prueba = line.split('/')
			socket.inet_aton(prueba[0])
			site = socket.gethostbyaddr(prueba[0])
			print "Direccion IP del sitio: " + prueba[0]
			print "Direccion URL del sitio: " + site[0]
		except socket.error:
			print "ip no valida"
	
	elif opt in ('-s', '--site'):
		line = arg
		try:
			prueba = line.split('/')
			print "Direccion IP del sitio: " + socket.gethostbyname(prueba[0])
			print "Direccion URL del sitio: " + line
				
		except:
			print 'sitio no valido'
	
	elif opt in ('-h','--help'):
		print '-p, --ip Direccion IP del sitio'
		print '-s, --site Direccion URL del sitio'
		print '-h, ---help Ayuda '
		sys.exit(2)		
			
	else:
		print 'opcion no valida'
		sys.exit(2)

