#!/usr/bin/python

import socks
import socket

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
socket.socket = socks.socksocket

def getaddrinfo(*args):
	return [(socket.AF_INET,socket.SOCK_STREAM,6,'',(args[0],args[1]))]

socket.getaddrinfo = getaddrinfo

import requests
headers = {
	'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'referer' : 'https://www.google.com'
}

#print  requests.get('https://check.torproject.org/',headers = headers).content
print  requests.get('http://httpbin.org/ip',headers = headers).content

