#!/usr/bin/env python

import requests
import argparse
import getpass
import urllib3
import json 

#Disable Security warning
urllib3.disable_warnings()

#host = input("host/IP = ")
#port = 8006

# Generate token 
url = "https://192.168.226.35:8006/api2/json/access/ticket?username=power@pam&password=qwerty123"
#url = "https://%s:%s/api2/json/access/ticket" % (host, port)

response = requests.post(url, verify=False) 
data = response.json()
cookie = (data['data']['ticket'])
csrf = (data['data']['CSRFPreventionToken'])

print(cookie)
print(csrf)















