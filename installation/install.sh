#!/bin/sh
apt-get update
apt-get install git python-pip python-argparse libxml2-dev libxslt-dev python-dev tor python-socksipy privoxy -y
pip install requests lxml wget termcolor gitpython 

s='y'
if /etc/init.d/privoxy restart; then
	echo 'Everything is ok with privoxy'
else
	echo 'Could the installer remove all files of privoxy and try it again? [y/n]'
	read privoxy
	if [ "$privoxy" = "$s" ];then
		apt-get --purge remove prixovy -y
		apt-get install prixovy -y
		sed -i 's/^#\(.*\)forward-socks5\(.*\)127.0.0.1/	 forward-socks5   \/               127.0.0.1:9050 \./g' /etc/privoxy/config
		if /etc/init.d/privoxy restart; then
			echo 'Everything is ok with privoxy now!'
		else
			echo 'Something went wrong, please chek your configurations and try again.'
		fi
	else
		echo 'Good luck! :,('
	fi
	
fi

if /etc/init.d/tor restart; then
	echo 'Everything is ok with tor'
	echo 'Enjoy the tool :D'
else
	echo 'Could the installer remove all files of tor and try it again? [y/n]'
	read tor
	if [ "$tor" = "$s" ];then
		apt-get remove --purge tor -y
		apt-get install tor -y
		sed -i 's/^#\(.*\)ControlPort/ControlPort/g' /etc/tor/torrc
		sed -i 's/^#\(.*\)CookieAuthentication/CookieAuthentication/g' /etc/tor/torrc
		if /etc/init.d/tor restart; then
			echo 'Everything is ok with tor now!'
			echo 'Enjoy the tool :D'
		else
			echo 'Something went wrong, please chek your configurations and try again.'
		fi
	else
		echo 'Good luck! :,('
	fi
	
fi
