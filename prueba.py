'''
from bs4 import BeautifulSoup
import urllib2

response = urllib2.urlopen('http://localhost/moodle332')
html = response.read()

soup = BeautifulSoup(html,'html.parser')
print soup
for link in soup.find_all('a'):
	#print(link.get('href'))
	print link.get('src')


#print soup.title
'''
import  mechanize
from bs4 import BeautifulSoup
import urllib2

i = 'admin'
j = 'hola123,'
br = mechanize.Browser()
br.open('http://localhost/ojs302/index.php/index/login')
br.select_form(nr = 0 )
br.form['username'] = i
br.form['password'] = j
br.submit()
print br.response().geturl()
