#!/usr/bin/python
import argparse
import socket
import re
import sys
import requests
import hashlib
from lxml import etree
from lxml import html
import wget
import os

readme = ''
arg = ''

def moodle(arg):
# Si el argumento tiene http(s)
	m = hashlib.md5()
	
	if 'http://' in arg or 'https://' in arg:
		req = requests.post(arg)
		webpage = html.fromstring(req.content)
		fav = webpage.xpath('//link[@rel="shortcut icon"]/@href')
		
		mod = re.sub(r'(\/theme\/(.*))','',fav[0])
		readme = requests.post(mod + '/README.txt')
		upgrade = requests.post(mod + '/lib/upgrade.txt')
		
		if upgrade.status_code == 200:
			regex = re.compile(r'===(.*)===')
			match = regex.search(str(upgrade.text))
			try:
				if match.group():
					print "La version del sitio: " + arg + " es: " + match.group(1)
					sys.exit
			except:
				files(arg)
			sys.exit
			
		else:
			if readme.status_code == 200:
				m.update(readme.text)
				hs =  m.hexdigest()
				files(arg,hs)
			else:
				files(arg,'')

# Si no tiene http(s) se pega a la direccion
	else:
		http =  re.sub(r'(^)','http://',arg)
		moodle(http)
		exit(2)
		


def files(arg,readme):
	
	m = hashlib.md5()
	elements = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href']
	versions = {  
		
		"3.3" : ['84979523ed75adbc1556f1977139cae2',
				'258e27081e3b0c7be0b3b71dabc2b849',
				'3c879fa8aa7edbba12bb795da1252cdd',
				'38799ac3273984d7e7679af00db3388c',
				'66a7ee2af42c1c2d9f0367ebfcb5d520',
				'e656956396d080b6d46a25eef86bcfb7',
				'43e4b947ad5155701cbb41bd94793405',
				'0b088cdd96bb785fb0e311b7a81ce3d4',
				'3d1254d6baf1b3395111efd1ed8fc5df', #README
				'4807e45c357cc33d41b1c3cce527870c'], #/lib/upgrade.txt
		
		"3.2" : ['827f6ccc7f5f1c980a58717911372000',
				'0fbac5f5d051f4a173095af9c17f2dea',
				'90db94c67bb914d1930e14c7ddf4d52f',
				'91bb20f6d2f129c2a3a2fd123f5e6ac8',
				'19557f056a188921ce40d89cab73a12',
				'688e64dad15173cac9837708e090f20',
				'3d1254d6baf1b3395111efd1ed8fc5df', #README
				'f2b4fe132564f4088cfa4e5be0d3347d'], #/lib/upgrade.txt
		
		"3.1" : ['827f6ccc7f5f1c980a58717911372000',
				'eb574c401659603b9e4bcec0b584ad7f',
				'825c7cad81683054ca9fbf96cf5d109f',
				'a9f71a5b1eed758817bcbde19d2f855c',
				'6c3216c195a0a008d1cffb5e5e76c726',
				'f4ea7f63589795336efc12f4d501f08',
				'65e47d141f3528bb90d4ac064aef7fc',
				'3d1254d6baf1b3395111efd1ed8fc5df', #README.txt
				'bb712eebfd017efbe48cafe5f205c86f'], #/lib/upgrade.txt
		
		"3.0" : ['9d57807e33dab546e05fb2c6ea0ef1cf',
				'80c3c5b4c6a78abea8946ba92d655089',
				'e01abc451b320f2e28b8f20a1d9ca8d0',
				'c58452e32382fd598decaab6f0e758e8',
				'4f3896dd8200b00982b18d1821fa2ea2',
				'624f7a95d7b81c5e69a90b30ef38324',
				'ff6b8d9f2320ff071a204dd62ed0ce2',
				'5ec853aaf8759920d4d777fe67ab7f67', #README.txt
				'edaed7eb4cf82911ada7fea42f01613f'], #/lib/upgrade.txt
		
		"2.9" : ['8641f91cface82d9c1bdd16517cbfb81',
				'c8064b986ef40c13a8afff8cbfbc05c8',
				'3546e3273d0ef9a0e50fcf01b143b3dc',
				'266ef0f3ff84ea96165bc153d10981ee',
				'6948935708fc57a1d91d17c62c7d5f82',
				'96bec8bf2b1ecd931eb0a1b091a32a4',
				'955a3090e9fea99343281399cc38bd4',
				'5ec853aaf8759920d4d777fe67ab7f67', #README
				'7befda0d552af8dc0a08627a07e3a072'], #/lib/upgrade.txt
		
		"2.8" : ['1af562cb83b90bc77ef317d76a0ddad8',
				'6ad7d9c00c28f81435469f3dad874f98',
				'6fd5e957a90a6ddedb10de99251debea',
				'5f0921cc20f9d20c3dbe1ed9090d6c40',
				'fef1b49beb1274687660374fd2643b7',
				'f5c8d726bf662ae93dd21af0465677a',
				'5ec853aaf8759920d4d777fe67ab7f67', #README
				'2c2a8b55a4abfef4783847d2d1b296d8'],  #/lib/upgrade.txt
		
		"2.7" : ['9afc07e33c0cae0e11c28d4bc7fbf9b3',
				'3c24a5cc96a15a4d9eef626fa34c6203',
				'5301c7f71d6f353a928f794c0b7d7e02',
				'92911dd68694852d5669e6544e8684f7',
				'8e873bd720e94f57231c92e52792d1f4',
				'7116c5fba3f2b10ee001e2b7433a65b',
				'8d67d7ae307364ef103c58e900de83b',
				'5ec853aaf8759920d4d777fe67ab7f67', #README
				'8620a1284bfbdea117ecb4627f81ff32'],  #/lib/upgrade.txt
		
		"2.6" : ['2185368fca3a577697f6385b789f20ce',
				'5a6b67563ddc74d0da74912367dfae18',
				'e59d201c05f61ccca20b67e6d755ad3b',
				'a957b9da6541aad578941e851928eb0c',
				'3eeccf647b5d84c520a76a69817f8504',
				'ee0009b9fa4aecf9af2ca6ae1254cdb0',
				'7c74fa5653a2a6931ad92251753f0b2',
				'4f0478bac6c69f8041b8a8cd623ca2d',
				'5ec853aaf8759920d4d777fe67ab7f67', #README
				'5a337315355190fd460012fe16acdc56'],  #/lib/upgrade.txt
		
		"2.5" : ['75c5dfa7c242aa772e2cab69bdcde6b7',
				'20a244cbe4ac480f0dd91a72dbf884d6',
				'77ecf78b183fe1afc99716721d050436',
				'44c9bc9ec7a7de8af29bf76af9ebe446',
				'56528112932076cd4528f4ce123f2d1',
				'3b3db528793dc4cdecdc75a622cab65',
				'5ec853aaf8759920d4d777fe67ab7f67',    #README
				'37a5256e9dc014125b101ccd4539f0ad'], #/lib/upgrade.txt
		
		"2.4" : ['2a610dfce388d1546cf8990529fdcbe1',
				'716c608d89aabde4cb1bbfb98a00802b',
				'f5f20266c70141de0a7987b2ff873611',
				'1650c2a202b1cf95bddaaf0ae7a410a4',
				'56bbbc96963f117a54ba5210b33c443',
				'03f0fb067d5624d1179bc0e94fbab52',
				'7fb7332f87fe7b4bdd9de752b4d3c044'], #README
		
		"2.3" : ['fa9979903e91cefaea86f3eafa2d9885',
				'd33fe26085052e3348a94f43b3b3236f',
				'02f8fa6fd9e8adf7cbbdb3210c7f711e',
				'5f484a9988523f5a1df4f85f23f76596',
				'04a95b1a679dd85c96c9d097b80a90c0',
				'87be6a924f97d43a0a532d9dd2df4ae5',
				'60b1e7ec8ea53ed54788e1fd7ca4481',
				'9d6dd66c94e616efe30cc5f71fb312b',
				'e8151e02fc3c4c988451de73804a3506',
				'7a00a990667f92fd91d064e57e454e19',
				'379ab2f158bc5e16f5abbeffb8fce400',
				'023fcf7bf25a807dd3ffd850077879c4',
				'5883f34932944afe4a84595bc61d10ab',
				'c988d48f5e0104311bd0945d6d0fc17',
				'7fb7332f87fe7b4bdd9de752b4d3c044'], #README
		
		"2.2" : ['08b2b1cb0a45bc705db87a37129be5f3',
				'e34b3549324f258d14b9f313d37c0d40',
				'63daa6b54303c91b6352bb5c7ec5e5ec',
				'd4d1f0c1398184f2cf9421322ac6dd4c',
				'032d9cdaf19c37654fe3fb5a7e61bb27',
				'a18d5570412c5142136347db9cbdfb3e',
				'0b2313f845cc60af2bb687665116f03',
				'cbfece02e5309c422cad6b0bde9da430',
				'192958755347ce779292d2c580114055',
				'ad521a39fbc3febd1dae50dc765cb113',
				'abe3883c2a40c25603fa63cb678f2f0e',
				'7c99e3f91d9ed63cf2757126cf9f05e4',
				'dc3d3f42e314616b607aedb65663d70',
				'7fb7332f87fe7b4bdd9de752b4d3c044'], #README
		
		"2.1" : ['67b7aa11f1a83dd7b6c9cb51d5fff7af',
				'b60fb7b8d3a6a0e2fba88f44f0dbeb2e',
				'b090f672e462119ca96af4a3d6515819',
				'04141c28a4a6c30d61d6ffac049fbc05',
				'4464c873c27746f45789ecb2e8b25705',
				'75907760f2b60dc30b55cbf5132c5c5a',
				'7452ec0ac427803151ef1629983290f',
				'df57147abf6a79532f7819357aa9a83',
				'8c30e4ae300d963236e373c1e1f3e723',
				'f22dd2bb4f562becb62f72f5740bfa27',
				'4a6a3b3629b6521db128a3da90534bec'
				'b9aec5276f867e9ba668787df8fc478e',
				'7a19d5a655cbbf97a4a36485990cc76d',
				'4e75023de9286af715ee62c8630148b',
				'7fb7332f87fe7b4bdd9de752b4d3c044'], #README
		
		"2.0" : ['67b7aa11f1a83dd7b6c9cb51d5fff7af',
				'b60fb7b8d3a6a0e2fba88f44f0dbeb2e',
				'f4d02c6ec6140869dcf438dcade6ebed',
				'986958b0ae4fc857955bea2e2486d702',
				'4ccdfb6897cc21ce7912ede02b29ae69'
				'e289ead82a14941b8d4a7359b4ec4768',
				'6a7903659706d1c7be7b8c457e72389',
				'8c30e4ae300d963236e373c1e1f3e723',
				'b30a8f8daa36c2914a4f0d7d27388224',
				'7fd61a593ff7cc0ff04c18f2b29e3d6c',
				'e06f45d224503bee4651ae9282846bb7',
				'd713b2eeaa0b7631202a04550fc29c05',
				'93329781f70e6789ad1f2f816c19d7d',
				'7fb7332f87fe7b4bdd9de752b4d3c044'], #README
		
		"1.9" : ['6cf4eee2ff86587fd1edc8105c3267a6',
				'2331de761ef8f240e28e779f0894a79c',
				'36b253f0bc585f7e1e7d489cec70d3f8',
				'd605fd8416da11d86374c0c07bc4474f',
				'146a3e97547fb36843db9032ae4b174a',
				'de33d2e9b6837a53bb1bd87ea51cac14',
				'109335a70ee0dc051c3f721c65bf42f6',
				'8d8df8e8dbacaa0dbe4158985c4dcf25',
				'4fe9e074673601fd9a17bdb9aa12522',
				'4c4a7b840ee1975ca9ea9ec7d1df0f78'], #README
				

		
		"1.8" : ['f99c9d9c62da7b974264e07fb218d41f',
				'a33bdcb8a48278028b70f3f594e9ba78',
				'08eb4e9826c1bcf180f198529648db22',
				'e64eee0878cf2dd8a40e1ea4ffb56d0a',
				'73a0701434c5af8143328acf3ec2288d',
				'34813dd887310c606fc7a31fbf4594b7',
				'0559eb3fae0c492e0e6d4a3e140cadaa',
				'6a020e8decb91e100caf33e667b9acbf',
				'f8bd82800975ce77f879d57103038ca',
				'661d0ea234ad38620dcfe57d95bf1510',
				'884136e32507390601045b52597834b3',
				'583e5f3057b4e44804d16d51f4a181d4'], #README
				

		
		"1.7" : ['2e91ec47ff7a5e102a54f0a16a23383b',
				'7a3b09b4df20f9bf27fed63b3d737763',
				'069c2c2a026875d88cb17eabe09e00bd',
				'1b490141d489807c2d60f95749dc2ad6',
				'b159f99b3d78b8445ef3de3a972b9294',
				'ac5b5f9d644090fa1a80c38ed8bcb3db',
				'7ffb266c1b810f4c82f6ee335473a2a7',
				'8cca9ba0565e58648c580b89809bc20f',
				'92157d076c1a42a5402199a92d974cd6',
				'd048aaf7d5372c0345b7dfdc44390b6',
				'01516700e48e32b82d585c4ed81b80d',
				'b21876108801757cdfc3437629d18187']} #README
	
	elements.append(readme)			
	res = requests.post(arg)
	webpage = html.fromstring(res.content)

	i = 0
	site =  re.sub(r'(http|https)://','',arg)
	site = re.sub(r'/(.*)','',site)
	dom  = site.split('.') # Extrae el dominio
	dom.pop(0)
	domain =  '.'.join(dom)

	for i in range(0,len(listFind)):
		for link in webpage.xpath(listFind[i]):
			if domain in link:
				req = requests.post(link)
				if req.status_code == 200 and i in range(2,3):
					try:
						filename = wget.download(link)
						m.update(filename)
						hs = m.hexdigest()
						elements.append(hs)
						os.remove(filename)
					except:
						continue
				
				else:
					try:
						m.update(req.text)
						hs =  m.hexdigest()
						elements.append(hs)
					except:
						continue
	
	
	for element in elements:
		for key,value in versions.iteritems():
			if element in value:
				print '\nVersion: ' + key
	



def getParams(arg):
	
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-u', '--url', help='Direccion URL del sitio')
					
	
	options = parser.parse_args()
	
	if len(sys.argv) == 1:
		print parser.print_help()
		
	
	elif '-u' in sys.argv or '--url':
		moodle(options.url)
		
		
getParams(arg)


