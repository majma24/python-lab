#!/usr/bin/env python

import requests
import getpass
import json
import urllib3


#Disable Security warning
urllib3.disable_warnings()

# Define HOST, Username & Password
HOST = input("HOST : ")
PORT = 8006
realm = "pam"
url = "https://%s:%s" %(HOST,PORT)

user = input("username : ")
username = user + "@" + realm
password = getpass.getpass()
credential = {"username":username, "password":password }

# Generate Token & Cookie

url1= url +"/api2/json/access/ticket" 
response = requests.post(url1, data=credential, verify=False)

if response.status_code == 200:
    data = json.loads(response.text.encode('utf8'))
    ticket = data['data']['ticket']
    crsf = data['data']['CSRFPreventionToken']
    print("respon status : ", response.status_code)
    print("===>> Generate Token and Cookie <<===")
    print("Ticket : ", ticket)
    print("Token : ", crsf)
else :
    print ("respon status : ", response.status_code)

# Get list VM
url2 = url + "/api2/json/cluster/resources?" 

cookie = {'PVEAuthCookie' : ticket}
header = {
    'Accept: */*',
    'Content-Type :application/json',
    'CSRFPreventionToken: str(crsf)' 
}

result = requests.get(url2, cookies = cookie, verify=False)
json_results = result.json()
raw_data = json.dumps(json_results, iterate=2)
print(raw_data)



