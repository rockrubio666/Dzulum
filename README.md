Tool Name (Pending)


Tool created to make pentest for Moodle & OJS content managers.
Also, the tool has the next modules to make its job:
	
	* Bruteforce: With this module, the tool tries to get the right credentials from the site.
	
	* Path directory bruteforcing: In this module, you can obtain the links that are in the site.
	
	* Tor: Because everyone needs to be anonymous.
	
	* Proxy: To fault someone else.
	
	* Report: Useful if you have bad memory.
	
	* Versions: Gets the version of the content manager and it's possible vulnerabilities.

To use these modules, you will have to download this github as continue:

	git clone https://github.com/rockrubio666/ProyectoFinal
	
After that, you should execute the file install.sh:

	./install.sh

And finally to be a hacker don't forget to check the help:

	./scanner.py --help

	 -h, --help            show this help message and exit
	 -a Set User Agent, --Agent Set User Agent 
						Lets to specify the User Agent use it in the requests, e.g.: -a 'Thunderstruck'
						
	 -B Login,UserField,PassField,User,Password,Message, --Bruteforce Login,UserField,PassField,User,Password,Message
                        Tries to obtain the credentials of the site, parameters could be files, e.g.: /login/index.php,username,password,Users,Passwords,'Invalid Login'
                        
	 -b RequestFile,User,Password,Message, --bruteFile RequestFile,User,Password,Message
                        Tries to obtain the credentials of the site, this option needs a file with request, e.g.: my_request,Users,Passwords,'Invalid Login'
                        
	 -d File, --directoryBforce File
                        Look for possible links and javascript in the index page with help of a file, e.g.: -c sitesFile
                        
	 -k ID Cookie, Cookie Value, --Cookie ID Cookie, Cookie Value
                        Lets to specify the Session Cookie use it in the requests, e.g.: -k 'My_Cookie','Cuki'
                        
	 -m URL, --moodle URL  Searches elements necessaries to get the version and determine the possible vulnerabilities, e.g.: -m https://example.com/moodle/
	 
	 -o URL, --ojs URL     Searches elements necessaries to get the version and determine the possible vulnerabilities, e.g.: -o https://example.com/ojs/
	 
	 -p Proxy IP,Port, --proxy Proxy IP,Port
                        Sends requests through proxy, e.g.: -p 169.69.69.69,6969
                        
	 -r Text,HTML,XML, --report Text,HTML,XML
                        Generates reports in TXT,HTML and XML from the results. They also could be sent via mail, e.g.: -r text,html,xml (The mail option will be asked when the program begins)
                        
	 -T, --tor         Makes requests through Tor socks, e.g.: -T
	 
	 -v [Number], --verbose [Number]
                        Shows differents depuration levels, from 1 to 3, e.g.: -v 3

Enjoy it! 
