#!/usr/bin/python

import hashlib
import re
import sys
import requests
from lxml import etree
from lxml import html


arg = sys.argv[1]
log = ''


def ojs(arg):
	req = requests.post(arg)
	page_source =  req.text
	regex = re.compile(r'(.*)("((.*)\/index.php\/index\/login(.*))")(.*)')
	match = regex.search(page_source)
	try:
		if match.group():
			log = match.group(2).replace("\"","")
			version(log)
	except:
		print 'nio'
		sys.exit(2)
	
	
		
def version(log):
	req = requests.post(log)
	page_source =  req.text
	regex = re.compile(r'(.*)(name="generator" content="(.*)")')
	match = regex.search(page_source)
	try:
		if match.group():
			print "La version del sitio: " + arg + " es: " + match.group(3)
	except:
		print 'nio'
		
	


def files(arg):
	m = hashlib.md5()
	elements = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src']
	
	js = {  "2.3.7" : ['a728a0ecf3d220c30ce9b7dccc82d63e',
				   '4d5a879373b442c000f7d7814bb8abd7',
				   '4eb3c3412061a1a8d69cb5de381fc87f',
				   '0891d82f6de853a83328d2aa34322431'],

		"2.3.8" : ['a728a0ecf3d220c30ce9b7dccc82d63e',
				'4d5a879373b442c000f7d7814bb8abd7',
				'4eb3c3412061a1a8d69cb5de381fc87f',
				'0891d82f6de853a83328d2aa34322431'],
				
		"2.4.0" : ['575bbf164dc5b03a5a4264d8714171c7',
				 '327cdd668bfe85e308c04bff0fbd9206',
				 'e6f0011d8e092bbf8cb25174d3c8e921',
				 '9e42adc8b31b2592f8e3d082db4faf3e',
				 '0e29ab716d2a4f1c78343055c4dd1d83',
				 '1f2567e23c0a6b45272b8f6c24fa8410',
			 	 'a46e4474e835008ca0b8aaf92ea49f4c',
		 		 'd3ca7fb92c24a52eaf7f157ff0419f70',
	 			 'a521f9aae90611966c189b1034864e70',
				 '8bdc3f5637d9f6b8d4c78fd08eee9178',
				 '4f89c4d276cc57a9760fd4ffd56de685',
				 'f2d6c65d2328e57b9f752b21c08f25e0'],
				 
		"2.4.1" : ['575bbf164dc5b03a5a4264d8714171c7',
				   '327cdd668bfe85e308c04bff0fbd9206',
				   'e6f0011d8e092bbf8cb25174d3c8e921',
				   '9e42adc8b31b2592f8e3d082db4faf3e',
				   '0e29ab716d2a4f1c78343055c4dd1d83',
				   '1f2567e23c0a6b45272b8f6c24fa8410',
				   'a46e4474e835008ca0b8aaf92ea49f4c',
				   'd3ca7fb92c24a52eaf7f157ff0419f70',
				   'a521f9aae90611966c189b1034864e70',
				   '8bdc3f5637d9f6b8d4c78fd08eee9178',
				   '4f89c4d276cc57a9760fd4ffd56de685',
				   'f2d6c65d2328e57b9f752b21c08f25e0'],

		"2.4.3" : ['575bbf164dc5b03a5a4264d8714171c7',
				'327cdd668bfe85e308c04bff0fbd9206',
				'e6f0011d8e092bbf8cb25174d3c8e921',
				'f97f721c25196709deb9df21d34fdfab',
				'9d2b720403a3336734d023507a8f1990',
				'83cf3b98144e9986cc6b6a2e6349bb64',
				'fdd061683f2ae1df74d5a4f63212d2ac',
				'217ef3fcfa4c51ceb08f924581f120ce',
				'71a179a7a0659e56bc19e290e35ad8ca',
				'475f47f314f81b251b9eb9f626f859ba',
				'd8f8e271d2da219d84d36247b3c95604',
				'5880f6b5c6e20bc19e7fd93064af85f8',
				'3ee49f9134d54a56d6dba47dbced022b',
				'3ce1d33046f684e1d84d767df3f095ba',
				'22d9cf27b91500b03bcccdaac90e93f4',
				'04444f4a566309d398bc582699e6bde5',
				'79d1532ba512b2eca884f93e1a5abe98',
				'8507ee0e92740a1538ff7c00a0fe1f8a',
				'cae4a163eb639fb466f268d1306050cb',
				'f21807a5a31b0217bf008305e0458f32',
				'995e16162a346327bb4ba6f62223c5d0',
				'1a7b7c9e3643f6a2db0b27e06b20fa35',
				'86cd9b5925394f97f1d5e6d4a14c567d'],
		
		"2.4.4" : ['575bbf164dc5b03a5a4264d8714171c7',
				'327cdd668bfe85e308c04bff0fbd9206',
				'e6f0011d8e092bbf8cb25174d3c8e921',
				'd5dedc19fd7140fd905479616d61a2aa',
				'287d99da27c80eeb59830784d8fd63d3',
				'e3697aa2adf26be9d3fad9eb5a046840',
				'82af72f2b3eb04c07a6d206cce99a35a',
				'8476a89773c2c1b77e3965067dbd5100',
				'c73a762d548754f022d038a9559612d0',
				'15e022a1ab1d8800377527d5403650d0',
				'fecc49c1d82a328086572d059b11510c',
				'2eac95e1d217d435b0d219008e359336',
				'78389573ed46867cb59874d9e2771473',
				'8ffc4cae7f44f2306b6781e4b39f832d',
				'cf94181b5f331a394d345284fa9c91c9',
				'223b14603a64303e3168c07e3ad6d293',
				'ad650ef4732dfc43891fceb1585b5c56',
				'e2d00e68804b1c9cfd3de2bbeb6eb857',
				'5567f74670e6fcd75b08fe73c52dc1c6',
				'a7242d35b7aaec3289a2da6d1ae654a2',
				'462503c62b63c40ecdb8af003d52a7af',
				'387915ddef58996fe2d47f15a5352ce9',
				'e576b2ea9b8e20c32571937cca1d07f2'],
				
		"2.4.5" : ['575bbf164dc5b03a5a4264d8714171c7',
				 '327cdd668bfe85e308c04bff0fbd9206',
				 'e6f0011d8e092bbf8cb25174d3c8e921',
				 'd5dedc19fd7140fd905479616d61a2aa',
				 '287d99da27c80eeb59830784d8fd63d3',
				 '34a6268c05d915f70b9d1a1b1378b377',
				 '89a8d174badab9e5a133ba460cc2df37',
				 'ff2e355c3b7374e9cec700b396a857fa',
				 '23ddd1e53342cc718d5e1d327b498383',
				 '12ccbfbf0870c4404526ce635174a3ea',
				 '208a6c62b60a210738c3ae4b96dbe1ca',
				 '8773728b905989b689bb8ab943a316b3',
				 'ae6411c2f2ef9d7b71a0f8d248bbd17e',
				 '9b8d3e03c9d510bd80b86321dfbd2db5',
				 'f0da8bcf0315c61de742803decf56ca9',
				 'd162d2730f933f44f8c411ab2672b6f1',
				 '10991dc26754727c0b56cd2cf5dd6391',
				 'ab56f696725dc8a2d61baba6b8bf99ad',
				 '3cb42a364482f8fb4bf1ebc9e70dcf74',
				 '6e9568a045688a2f123a7d5e24f1cd4e',
				 'e49153d54250f07304a0439d6f9210f4',
				 '313a42b70173033ccab787f39ec04314',
				 'd8e4d5a3217d58f9bffeb643105a58ed'],
	
		"2.4.6" : ['575bbf164dc5b03a5a4264d8714171c7',
				'327cdd668bfe85e308c04bff0fbd9206',
				'e6f0011d8e092bbf8cb25174d3c8e921',
				'1bdb98e7ce9e78202ab67b0ff34aac2d',
				'bbec104b0e7c05317fbc553ccf4eae7e',
				'444c4bd9c64a57e941d98fa90fda9731',
				'b69c9503bce181de3221c662f60f7ec2',
				'7e051560bd0cc77cff7a2bf7ce7263c0',
				'36d981f7243f0f86ff34ec74bfb76261',
				'1cd15078e574e2b786020357f96257b1',
				'91df3aec261d90e90df5078d595fbc85',
				'124e05968a8649077dda68562d357850',
				'3f5d762faf267ac6ef4dda3cdd632aa8',
				'f6371570d6d771370992781402ee2953',
				'f74b95fe90d93bdd6d696aa2de8c187a',
				'c7d420c91c7c40ef0fc236f2867e8983',
				'6a194159f4e4a4c321348158fb56f77e',
				'3a0bf4989129e956370dbbfac81d6393',
				'c96318f166b5bf54cd7bae3258f67458',
				'e2ff6047624a441b946048e94bd69e54',
				'3dfeceb8fbe347ef1cb4ecc078553757',
				'13adca952a8b74c21a01c7f0aa7489d1',
				'9357302dbe74f2a1104cabe3b557c16d'],
				
		"2.4.7" : ['575bbf164dc5b03a5a4264d8714171c7',
				 '327cdd668bfe85e308c04bff0fbd9206',
				'e6f0011d8e092bbf8cb25174d3c8e921',
				'1bdb98e7ce9e78202ab67b0ff34aac2d',
				'bbec104b0e7c05317fbc553ccf4eae7e',
				'444c4bd9c64a57e941d98fa90fda9731',
				'b69c9503bce181de3221c662f60f7ec2',
				'7e051560bd0cc77cff7a2bf7ce7263c0',
				'36d981f7243f0f86ff34ec74bfb76261',
				'1cd15078e574e2b786020357f96257b1',
				'91df3aec261d90e90df5078d595fbc85',
				'124e05968a8649077dda68562d357850',
				'3f5d762faf267ac6ef4dda3cdd632aa8',
				'f6371570d6d771370992781402ee2953',
				'f74b95fe90d93bdd6d696aa2de8c187a',
				'c7d420c91c7c40ef0fc236f2867e8983',
				'6a194159f4e4a4c321348158fb56f77e',
				'3a0bf4989129e956370dbbfac81d6393',
				'c96318f166b5bf54cd7bae3258f67458',
				'e2ff6047624a441b946048e94bd69e54',
				'3dfeceb8fbe347ef1cb4ecc078553757',
				'13adca952a8b74c21a01c7f0aa7489d1',
				'9357302dbe74f2a1104cabe3b557c16d'],
		
	   "2.4.8" : [ '575bbf164dc5b03a5a4264d8714171c7', 
				'327cdd668bfe85e308c04bff0fbd9206',
				'e6f0011d8e092bbf8cb25174d3c8e921',
				'2230df8e07947413dfa76fcc138243b0',
				'c415c787ba4380ca9053cf09743202ac',
				'ee6dc36a8097372fc92778236c032b0b',
				'83b95a24f05fdbc0c69dee0ad9f83e29',
				'154947b27cfd76becfebea70809d600f',
				'33725eafc8af3a49fae7da4678e50b49',
				'9cddcb460c51cc38fb2fc3fbaadb0c47',
				'9b8c2ce589a0463630f4ffa6e34eceb6',
				'c307802230435ae3c23e6c734b0b8fe3',
				'ff08d351662f155c3f391b176300840d',
				'6f6fd5b2c3b48cf21815822a950cce28',
				'9a5c70320dbf03917f949efd2297f60c',
				'3802710346b2aa8e9b95b5b94e83e1ae',
				'8c556705bf81eb36e197dc58832a8499',
				'8b896726c9798a596a15e22d77579670',
				'83d6abde8c2b1c9078d8d7ebe9c23ec5',
				'1072568e5e34f6248362968575ab03dd',
				'094a8928109295742d46a67d4e1a4176',
				'26a18c1f295a9868494a5a6b76b743fa',
				'50e34fd34588f3a3a839b5d8482f76f5'],
				
		"3.0.2" : ['b0ea462d35bf9562497345655b1a1a0c',
				   '898f59067992e0a8124fbbc2c073cf2c']}
	
	css = { "2.3.7" : ['ae0daf35fd83499b0660a2c05bad2a09',
				'2951da4bfc58790a202e3f41e6dcdb0f',
				'6cc27529b60a1b27b49b558e401d509b',
				'ba87592c4b99cc8b31dead8461423a5a',
				'3de5ca485cf588415c99befd37e86f37'],
				
		"2.3.8" : ['ae0daf35fd83499b0660a2c05bad2a09',
				'2951da4bfc58790a202e3f41e6dcdb0f',
				'6cc27529b60a1b27b49b558e401d509b',
				'ba87592c4b99cc8b31dead8461423a5a',
				'3de5ca485cf588415c99befd37e86f37'],
				
		"2.4.0" : ['ce9ae3134e86687c9f435ee97ac1843b',
				'b4d18405cc01a91fba05642f06f7d687',
				'a253bfbec97d679d83f9b03b2d1eaa74',
				'ea2b86521d24f5726289b5c2988eacaf',
				'53782ed3741d65b84528923313a347c0',
				'49e2e22c149cbdb61b9009eda4f7e8af'],

		"2.4.1" : ['ce9ae3134e86687c9f435ee97ac1843b',
				'b4d18405cc01a91fba05642f06f7d687',
				'a253bfbec97d679d83f9b03b2d1eaa74',
				'ea2b86521d24f5726289b5c2988eacaf',
				'53782ed3741d65b84528923313a347c0',
				'49e2e22c149cbdb61b9009eda4f7e8af'],
				
		"2.4.2" : ['105fe52d0a376018b8eeba9ac4a286a9',
				'2fd881bd435fdb5a86d5f8fd57fb5ba8',
				'128566940998660da1c9673b88382add',
				'83bceeaa6746f4ea125490d8b2376bf0',
				'619bcd92ec1c27248f1955bdf559ca02',
				'ecd29a9f3ede3b7d6f98db621f0900f8'],
				
		"2.4.3" : ['c1bf66c38ec2e50e55db0d82c4a388d8',
				'd9a7ffc712e4e227853eb9833a689c47',
				'ae0cd6570312cd106989a1cd7d58a51c',
				'26a98cb2bb619c9a5f71b69f555b8ede',
				'bf376d07e9a6762fa80e665a5481c392',
				'bf255d62c5f374c9b6e87e0907cfcec4'],
				
		"2.4.4" : ['9386a2da0d85b4a5e26a1637db3e54a7',
				'0eee248118572387bf511675e1d32723',
				'8436a250452061a9cba000f35a0c598d',
				'e938e34f502933594633761797b6ba51',
				'81edeb75afc1cc56737781579cb87064',
				'b9955837b7145585064e8d98a9b9b415',
				'92ef341f31e62d902e90cbed2214f625'],
				
		"2.4.5" : ['9386a2da0d85b4a5e26a1637db3e54a7',
				'0eee248118572387bf511675e1d32723',
				'6005c209986f53288260702786727299',
				'62cc7d93a4fac69ce3a9d0cfac8b063e',
				'64208984de482391251d0ee51914fb1b',
				'73f597562e3002214672fa1dd7bba930',
				'b7bd502232c318098e6ce46381d82717'],
				
		"2.4.6" : ['0231872d954707b6009758d77a4795f0',
				'4c6847eff0f6345d3eab3582751af7c7',
				'8164900a8b4226b9b6a21e319663685b',
				'23b12b0e3a759c656c59db52393890d8',
				'380182e45bf34e37e2be41a85e44c961',
				'204920a1b3bc2628fc1123fcc134fd6e',
				'949f18832d10d7fc742bd6370763e014'],
				
		"2.4.7" : ['0231872d954707b6009758d77a4795f0',
				'4c6847eff0f6345d3eab3582751af7c7',
				'8164900a8b4226b9b6a21e319663685b',
				'23b12b0e3a759c656c59db52393890d8',
				'380182e45bf34e37e2be41a85e44c961',
				'204920a1b3bc2628fc1123fcc134fd6e',
				'949f18832d10d7fc742bd6370763e014'],
				
		"2.4.8" : ['08a481aaa1e7c3df7c12b9ccfc6f4cfb',
				'2c207fdf610ffde9c54167c4c2ed14d8',
				'50b08c42387d02499736f9da90a87291',
				'1a65bc4d2ad4e14634aaa857dc8d6c12',
				'e31f8fe5668cf5cc44c2928aa5a85feb',
				'706f2e680e3bc47e32fbba83086ec789',
				'19454fa2ab19dc33aabc98bced3b1ce0'],
				
		"3.0.2" : ['6db1ce44ab7ab1d7263851bf7e94af37']}
	
	img = { "3.0.2" : ['/templates/images/structure/logo.png',
				'/templates/images/ojs_brand.png',
				'/lib/pkp/templates/images/pkp_brand.png']}

	
	res = requests.post(arg)
	page_source = res.text
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
				if req.status_code == 200:
					try:
						m.update(req.text)
						hs =  m.hexdigest()
						
						elements.append(hs)
					except:
						continue
						
									
	for element in elements:
		for key,value in js.iteritems():
			if element in value:
				print key
		

files(arg)
