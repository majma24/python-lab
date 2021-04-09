#!/usr/bin/env python

import requests
import json
import urllib3
import getpass

urllib3.disable_warnings()

host = input("Hosts : ")
port = 8006
url = "https://%s:%s" % (host,port)

user = input("username : ")
realm = "pam"
username = user + "@" + realm

password = getpass.getpass()
    
credential = {"username":username, "password":password}
url2 = url + "/api2/json/access/ticket"

response = requests.post(url2, verify=False, data=credential)
response = json.loads(response.text)
print(response)





