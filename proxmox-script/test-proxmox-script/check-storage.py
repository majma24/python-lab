#!/usr/bin/env python

import requests
import json
import csv
import urllib3
from decouple import config
from hurry.filesize import size
from prettytable import PrettyTable

# Disable Security warning
urllib3.disable_warnings()

HOST = input("HOST : ")
PORT = 8006
url = "https://%s:%s" %(HOST,PORT)

realm = "pam"
user = config('username')
password = config('password')
username = user + "@" + realm
credential = {"username":username, "password":password }
print("\n")
   
# Generate Token
url1= url +"/api2/json/access/ticket" 
response = requests.post(url1, data=credential, verify=False)
data = json.loads(response.text.encode('utf8'))
data2 = json.dump(data, open("data2.json", "w"), sort_keys=True, indent=4)
if not response.ok:
    raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))

ticket = data['data']['ticket']
crsf = data['data']['CSRFPreventionToken']
clustername = data['data']['clustername']

# Get Storage Info

url1 = url + "/api2/json/resource?type=storage"
cookie = {'PVEAuthCookie' : ticket}
header = {
    'Accept': '*/*',
    'Content-Type' :'application/json',
    'CSRFPreventionToken': str(crsf) 
}

result = requests.get(url1, cookies = cookie, headers= header, verify=False)
data = result.json()
r_data1 = json.dump(data, open("storage.json","w"), indent=4, sort_keys=True)
r_data = json.dumps(data, indent=4, sort_keys=True)
r_datavm = json.loads(r_data)
print(result)


