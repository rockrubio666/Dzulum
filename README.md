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
                        User Agent value
	
	-B Login,UserField,PassField,User,Password,Message, --Bruteforce Login,UserField,PassField,User,Password,Message
                        Login = Url Login, User= Value or file, Password= Value o file, Message= Error Message
	
	-b RequestFile,User,Password,Message, --bruteFile RequestFile,User,Password,Message, User= Value or file, Password= Value o file,
                        Message= Error Message
                        
	-c File, --crawlerHead File
                        File with directories
	-C, --Crawler         Crawling site
	
	-k ID Cookie, Cookie Value, --Cookie ID Cookie, Cookie Value
                        Cookide ID,Cookie value
                        
	-m URL, --moodle URL  URL from Moodle site
	
	-o URL, --ojs URL     URL from OJS site
	
	-p Proxy IP,Port, --proxy Proxy IP,Port
							Proxy
							
	-r Text,HTML,XML, --report Text,HTML,XML
                        Reports the results getting from the site
                        
	-T, --tor             Use Tor
	
	-v [Number], --verbose [Number]
                        Verbose Level 1-3
