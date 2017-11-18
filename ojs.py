#!/usr/bin/python

import hashlib
import re
import sys
import requests
from lxml import etree
from lxml import html
import wget
import os
from collections import Counter
import operator
from termcolor import colored,cprint

arg = sys.argv[1]

readmeFiles = ['2.0.1','2.0.2','2.1.0','2.1.1','2.2.0','2.2.1','2.2.3','2.3.0','2.3.1','2.3.2','2.3.4','2.3.5',
			'2.3.6', '2.3.7','2.4.0','2.4.1','2.4.2','2.4.3','2.4.4','2.4.5','2.4.6','2.4.7','2.4.8',
			'3.0', '3.0b', '3.0.1', '3.0.2','BEACON']

changeFiles = ['2.0.1', '2.0.2', '2.1', '2.1.1', '2.2', '2.2.1', '2.3.0', '2.3.3', '2.3.4', '2.3.5', '2.3.6'
				'2.3.7', '2.3.8', '2.4.0', '2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5']

pluginDefault = ['/generic/lucene/README' , '/gateways/resolver/README', '/reports/subscriptions/README', 
				'/generic/counter/README', '/generic/openAds/README','/generic/tinymce/README',
				'/generic/staticPages/README', '/generic/customBlockManager/README', '/implicitAuth/shibboleth/README-Shibboleth',
				'/generic/pdfJsViewer/README', '/generic/googleAnalytics/README.md', '/importexport/crossref/README',
				'/importexport/datacite/README', '/importexport/medra/README', '/importexport/pubmed/README',
				'/generic/orcidProfile/README.md', '/generic/webFeed/README', '/generic/addThis-master/README.md',
				'/generic/piwik-master/README.md', '/generic/ojs3-markup-master/README.md', '/generic/defaultTranslation-ojs-dev-2_4/README',
				'/generic/translator-master/README', '/generic/makeSubmission-master/readme.md', '/generic/reviewReport-master/README.md',
				'/generic/citationStyleLanguage-master/readme.md', '/generic/coins-master/README.md', '/generic/ojs-markup-master/README.md',
				'/generic/ojs-plum-plugin-master/README.md']
versions = {  
		"2.3.5" : ['384772142d1907d7d3aea3ac11fad9d0',
					'7d640303ec1bd0a376999f6e75f63c8d',
					'65501be7c096bbe4646d5d3e9e345e62',
					'f2e2f0c833643d76e4d923a86090ad35',
					'4bdfef55f0a90d4b497a8a4207e3ff2b',
					'66b6e69e47cee7e4d29a060b2a3c1da7',
					'62efe9c068785969b1e8cb9ae9da83ed',
					'1a3ddae3e99a081b70e05f8c33a6f96a',
					'42e8ee2a3108a7891cde5f4c9791cdaf',
					'f467f73c54fc5f27df5e54fd405f448a'],
	
		"2.3.6" : ['384772142d1907d7d3aea3ac11fad9d0',
					'7d640303ec1bd0a376999f6e75f63c8d',
					'65501be7c096bbe4646d5d3e9e345e62',
					'f2e2f0c833643d76e4d923a86090ad35',
					'4bdfef55f0a90d4b497a8a4207e3ff2b',
					'66b6e69e47cee7e4d29a060b2a3c1da7',
					'62efe9c068785969b1e8cb9ae9da83ed',
					'1a3ddae3e99a081b70e05f8c33a6f96a',
					'42e8ee2a3108a7891cde5f4c9791cdaf',
					'f467f73c54fc5f27df5e54fd405f448a',
					'3f262048db4232ff166095b7535c7872'],
	
	
		"2.3.7" : ['a728a0ecf3d220c30ce9b7dccc82d63e',
				   '4d5a879373b442c000f7d7814bb8abd7',
				   '4eb3c3412061a1a8d69cb5de381fc87f',
				   '0891d82f6de853a83328d2aa34322431',
				   'ae0daf35fd83499b0660a2c05bad2a09',
				   '2951da4bfc58790a202e3f41e6dcdb0f',
				   '6cc27529b60a1b27b49b558e401d509b',
				   'ba87592c4b99cc8b31dead8461423a5a',
				   '3de5ca485cf588415c99befd37e86f37',
				   '8066ea1c35d4148fdb30c605d71f315c'],

		"2.3.8" : ['a728a0ecf3d220c30ce9b7dccc82d63e',
				'4d5a879373b442c000f7d7814bb8abd7',
				'4eb3c3412061a1a8d69cb5de381fc87f',
				'0891d82f6de853a83328d2aa34322431',
				'ae0daf35fd83499b0660a2c05bad2a09',
				'2951da4bfc58790a202e3f41e6dcdb0f',
				'6cc27529b60a1b27b49b558e401d509b',
				'ba87592c4b99cc8b31dead8461423a5a',
				'3de5ca485cf588415c99befd37e86f37'],
				
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
				 'f2d6c65d2328e57b9f752b21c08f25e0',
				 'ce9ae3134e86687c9f435ee97ac1843b',
				'b4d18405cc01a91fba05642f06f7d687',
				'a253bfbec97d679d83f9b03b2d1eaa74',
				'ea2b86521d24f5726289b5c2988eacaf',
				'53782ed3741d65b84528923313a347c0',
				'49e2e22c149cbdb61b9009eda4f7e8af',
				'84bb8f3d3d8f6e4a2005f72966960936'],
				 
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
				   'f2d6c65d2328e57b9f752b21c08f25e0',
				   'ce9ae3134e86687c9f435ee97ac1843b',
				'b4d18405cc01a91fba05642f06f7d687',
				'a253bfbec97d679d83f9b03b2d1eaa74',
				'ea2b86521d24f5726289b5c2988eacaf',
				'53782ed3741d65b84528923313a347c0',
				'49e2e22c149cbdb61b9009eda4f7e8af',
				'3787a97f2aafca5f793806a1196fdd00'],
				
		"2.4.2" : ['575bbf164dc5b03a5a4264d8714171c7',
				'327cdd668bfe85e308c04bff0fbd9206',
				'e6f0011d8e092bbf8cb25174d3c8e921',
				'4bb0100702a8e376906e821bbfef0d5c',
				'87543c2f0a759c049e9bc604d33f71b2',
				'bfa0f2db7fffe134d0036df368fc5c2a',
				'63f7aaf40cd654ce09a966d31ddf0cbe',
				'22579d0377978d7f1a32d9155c74f7a3',
				'c20ce89f20bb36cb8454594e45d8a3eb',
				'72d71affbc191a805148a08feed66105',
				'74970e548eaf5354216dce5165c7e652',
				'69efe8afc38ae44ee030d0c9a1aad90b',
				'2c4ca2a6f23d53ab58576aeb58ce283d',
				'a4e96c3ad33d9714fa2139d3dd475e88',
				'3e193a54a00a5122890484e595f47f64',
				'50183aa9790394c91a0ffb00cd8f61ad',
				'5a98465baf74321256e20db000fc2654',
				'a4409801f5d20f6437fc895246f62547',
				'5e3533f747e8c110dbb46db898a98b93',
				'1c9b997e1d842cdbedffeac3e02f51bc',
				'1d9366fe647f81f49309abb2ba4311ee',
				'fbd52ac399a24bc77eb0ff531a827593',
				'24b772e55f13eaddc9f87ad501c0fbef',
				'eb2e1f0af749d00a477e0c6cb5902b46',
				'e8506f2c3a32ac2cfcf2b2c62d9e4edf',
				'112aec7c26478ae58c7a4c1d804d3a41',
				'2173265fd5089e9a2076c02cca5e458f',
				'64cb7704a61ef9fc3718bbf4fd24a66e'],

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
				'86cd9b5925394f97f1d5e6d4a14c567d',
				'c1bf66c38ec2e50e55db0d82c4a388d8',
				'd9a7ffc712e4e227853eb9833a689c47',
				'ae0cd6570312cd106989a1cd7d58a51c',
				'26a98cb2bb619c9a5f71b69f555b8ede',
				'bf376d07e9a6762fa80e665a5481c392',
				'bf255d62c5f374c9b6e87e0907cfcec4',
				'e27c5b0b0607d5eeebf3c30ea63cac41'],
		
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
				'e576b2ea9b8e20c32571937cca1d07f2',
				'9386a2da0d85b4a5e26a1637db3e54a7',
				'0eee248118572387bf511675e1d32723',
				'8436a250452061a9cba000f35a0c598d',
				'e938e34f502933594633761797b6ba51',
				'81edeb75afc1cc56737781579cb87064',
				'b9955837b7145585064e8d98a9b9b415',
				'92ef341f31e62d902e90cbed2214f625',
				'36c11c67c4fa54e575835f309e9c7a97'],
				
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
				 'd8e4d5a3217d58f9bffeb643105a58ed',
				 '9386a2da0d85b4a5e26a1637db3e54a7',
				'0eee248118572387bf511675e1d32723',
				'6005c209986f53288260702786727299',
				'62cc7d93a4fac69ce3a9d0cfac8b063e',
				'64208984de482391251d0ee51914fb1b',
				'73f597562e3002214672fa1dd7bba930',
				'b7bd502232c318098e6ce46381d82717',
				'503026a5450579ac88198efd9f95282e'],
	
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
				'9357302dbe74f2a1104cabe3b557c16d',
				'0231872d954707b6009758d77a4795f0',
				'4c6847eff0f6345d3eab3582751af7c7',
				'8164900a8b4226b9b6a21e319663685b',
				'23b12b0e3a759c656c59db52393890d8',
				'380182e45bf34e37e2be41a85e44c961',
				'204920a1b3bc2628fc1123fcc134fd6e',
				'949f18832d10d7fc742bd6370763e014',
				'd19062c6da8ce2d1ea31d64e2506d1f9'],
				
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
				'9357302dbe74f2a1104cabe3b557c16d',
				'0231872d954707b6009758d77a4795f0',
				'4c6847eff0f6345d3eab3582751af7c7',
				'8164900a8b4226b9b6a21e319663685b',
				'23b12b0e3a759c656c59db52393890d8',
				'380182e45bf34e37e2be41a85e44c961',
				'204920a1b3bc2628fc1123fcc134fd6e',
				'949f18832d10d7fc742bd6370763e014',
				'b37bf69c27af1c26802a75c88351e67f'],
		
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
				'50e34fd34588f3a3a839b5d8482f76f5',
				'08a481aaa1e7c3df7c12b9ccfc6f4cfb',
				'2c207fdf610ffde9c54167c4c2ed14d8',
				'50b08c42387d02499736f9da90a87291',
				'1a65bc4d2ad4e14634aaa857dc8d6c12',
				'e31f8fe5668cf5cc44c2928aa5a85feb',
				'706f2e680e3bc47e32fbba83086ec789',
				'19454fa2ab19dc33aabc98bced3b1ce0',
				'2d500cf27b84bf8101ecc8c1d03f0f0b'],
		
		"3.0.0"	: ['b0ea462d35bf9562497345655b1a1a0c',
					'3f2861b8ec7fb6c91cba210bc7a8d161',
					'130da13d6103618eb7d45de190c30acb'
					'950cf73a5f601dbc1aceea9367bb4de',
					'125c862647362c7d205bd889889ce9c',
					'd529d69d1df57044affe4f79a4eee24',
					'9fa541c3add9fa089f1c4cf50f4c007c'],
					
		"3.0.1" : ['b0ea462d35bf9562497345655b1a1a0c',
					'3f2861b8ec7fb6c91cba210bc7a8d161',
					'8caf3662ce236d44a7edb1f900a1e04a'
					'950cf73a5f601dbc1aceea9367bb4de',
					'125c862647362c7d205bd889889ce9c',
					'd529d69d1df57044affe4f79a4eee24',
					'7c91b09ebdaac33137c763f06b709c2c'],
					
		"3.0.2" : ['b0ea462d35bf9562497345655b1a1a0c',
				   '898f59067992e0a8124fbbc2c073cf2c',
				   '6db1ce44ab7ab1d7263851bf7e94af37'
				   '0c384bedcc1e813c9dc96665fd5b0c1',
				   'bb87d41d15fe27b500a4bfcde01bb0e',
				   '4e3706431052055bcd3aed2a06479b0',
				   '293231fd3b3a687dc6dd6be0fdddca59']}
	
def ojs(arg):
	requests.packages.urllib3.disable_warnings()
	req = requests.post(arg, verify=False)
	page_source =  req.text
		
	regex = re.compile(r'(.*)(name="generator") content="(.*)"(.*)')
	match = regex.search(page_source)
	try:
		if match.group():	
			print "La version del sitio: " + colored(arg, 'green') + " es: " + colored(match.group(3),'green')
			print "Version del sitio encontrada en:" + colored(match.group(),'green')
			files(arg)
		exit
	except:
		version(arg)

def version(arg):
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href']
	
	requests.packages.urllib3.disable_warnings()					
	res = requests.post(arg, verify=False)
	
	webpage = html.fromstring(res.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)):
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				req = requests.post(link)
				if req.status_code == 200 and i in range(2,3):
					try:
						filename = wget.download(link, bar=None)
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
				average.append(key)
				
	cnt = Counter(average)
	print '\nVersion del sitio aproximada mediante archivos de configuracion: ' + colored(max(cnt.iteritems(),key=operator.itemgetter(1))[0], 'green')
	files(arg)
	
	
def files(arg):
	listThemes = ['//script/@src', '//@href']
	tmp = []
	requests.packages.urllib3.disable_warnings()					
	for element in pluginDefault:
		plugin = arg + '/plugins' + element
		req = requests.post(plugin, verify=False)
		if req.status_code == 200:
			plugName = re.compile(r'=== (.*)')
			pN = plugName.search(req.text)
			plugVers = re.compile(r'(===) (Version(.*))')
			pV = plugVers.search(req.text)
			try:
				if pN.group():	
					try:
						if pV.group():
							print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green') + " " + colored(pV.group(2), 'blue')
					except:
						print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green')
				
			except:
				continue
					
			regex = re.compile(r'(.*)\/(.*)\/README(.*)')
			match = regex.search(plugin)
			try:
				if match.group():
					print "Plugin, Name: " + colored(match.group(2), 'green') + ' ,Path: ' + colored(plugin, 'green')
			except:
				continue
				
		else:
			continue
	
	
	for element in readmeFiles:
		readme = arg + '/docs/release-notes/README-' + element
		req = requests.post(readme, verify=False)
		if req.status_code == 200:
			print 'README file: ' + colored(readme, 'green')
		else:
			continue
			
	for element in changeFiles:
		changeLog = arg + '/docs/release-notes/ChangeLog-' + element
		req = requests.post(changeLog, verify= False)
		if req.status_code == 200:
			print 'ChangeLog: ' + colored(changeLog,'green')
		else:
			continue
	
	req = requests.post(arg + '/robots.txt', verify=False)
	if req.status_code == 200:
		print 'Robots file: ' + colored(req.url, 'green')
	
	
	res = requests.post(arg, verify=False)
	webpage = html.fromstring(res.content)
	for i in range(0,len(listThemes)):
		for link in webpage.xpath(listThemes[i]):
			if 'theme' in link or 'journals' in link or 'themes' in link:
				tmp.append(link)
			else:
				continue
				
	for element in range(0,len(tmp)):
		if 'default' in tmp[element]:
			print colored( 'Default Theme', 'green') + ' Path: ' + colored(tmp[element], 'green')
			element + i
		elif 'journals' in tmp[element]:
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():	
					print 'Customize Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
					element + 1
			except:
				pass
		elif 'theme' in tmp[element]:
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():	
					print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
			except:
				pass	
		elif 'bootstrap' in tmp[element]:
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():	
					print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
			except:
				pass	
		else:
			sys.exit
		
			

ojs(arg)


