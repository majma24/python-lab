#!/usr/bin/env python

import requests
import json
import time
from decouple import config
import urllib3

# Disable Security warning
urllib3.disable_warnings()

# Global Username 
realm = "pam"
user = config('username')
password = config('password')
username = user + "@" + realm
credential = {"username":username, "password":password }
PORT = 8006
filename = "inventory.txt"

def load_file():
    
    with open(filename, 'r') as fp:
        for count, ip in enumerate(fp):
            ip = ip.strip()
            #url = "https://"+ip+":"+str(PORT)
            return ip


def auth():
    url1= url +"/api2/json/access/ticket" 
    response = requests.post(url1, data=credential, verify=False)
    data = json.loads(response.text.encode('utf8'))
    data2 = json.dump(data, open("data2.json", "w"), sort_keys=True, indent=4)
    if not response.ok:
        raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))

    ticket = data['data']['ticket']
    crsf = data['data']['CSRFPreventionToken']
    clustername = data['data']['clustername']

    print("clustername : ", clustername)
    print("ticket : ", ticket)
    print("crsf : ", crsf)
    

generate_data = auth()



