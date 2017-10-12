import requesocks

session = requesocks.session()

session.proxies = {'http':'socks5://localhost:9050', 'https' : 'socks5://localhost:9050'}

response = session.get('http://icanhazip.com')
print response.text
