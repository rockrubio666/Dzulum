import requests

proxies = {'http:' : 'http://127.0.0.1:8080',
			'https:' : 'http://127.0.0.1:8080'}
			
r = requests.head('https://www.becarios.unam.mx', proxies=proxies)
print r.headers
print r.text
print r
