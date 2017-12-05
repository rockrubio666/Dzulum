#!/bin/sh
apt-get update
apt-get install git python-pip python-argparse libxml2-dev libxslt-dev python-dev tor python-socksipy privoxy -y
pip install requests lxml wget termcolor gitpython 

sed -i 's/^#\(.*\)ControlPort/ControlPort/g' /etc/tor/torrc
sed -i 's/^#\(.*\)CookieAuthentication/CookieAuthentication/g' /etc/tor/torrc
sed -i 's/^#\(.*\)forward-socks5\(.*\)127.0.0.1/	 forward-socks5   \/               127.0.0.1:9050 \./g' /etc/privoxy/config

/etc/init.d/tor restart
/etc/init.d/privoxy restart
