#!/usr/bin/python


import urllib2

from stem import Signal
from stem.control import Controller
import requests

#from config.config import *

def renew_ip():
 with Controller.from_port(port=9051) as controller:
	 controller.authenticate()
	 controller.signal(Signal.NEWNYM)
	 print 'controller'
#	print requests.get('http://httpbin.org/ip', proxies=proxies).text

def send_request():
	renew_ip()
	session = requests.Session()
	session.proxies = {'http':'localhost:8118'}
	response = session.get('http://httpbin.org/ip', timeout=2)
	print response.text
	pass
	
	
for tmp in list(range(0,20)):
	send_request()
	
	
'''
proxy = urllib2.ProxyHandler({'http' : '127.0.0.1:8118'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)


'''

'''
import requesocks
session = requesocks.session()

session.proxies = {'http':'socks5://localhost:9050','https':'socks5://localhost:9050'}
response = session.get('http://icanhazip.com')
print response.text
'''
