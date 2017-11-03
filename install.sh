#!/bin/sh
apt-get update
apt-get install git python-pip python-argparse libxml2-dev libxslt-dev python-dev tor privoxy -y
pip install requests lxml stem wget

sed -i 's/^#\(.*\)ControlPort/ControlPort/g' /etc/tor/torrc
sed -i 's/^#\(.*\)CookieAuthenticacion/CookieAuthenticacion/g' /etc/tor/torrc
sed -i 's/^#\(.*\)forward-socks5\(.*\)127.0.0.1/	 forward-socks5   \/               127.0.0.1:9050 \./g' /etc/privoxy/config

/etc/init.d/tor restart
/etc/init.d/privoxy restart
/etc/init.d/networking restart
