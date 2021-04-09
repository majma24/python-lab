#!/usr/bin/env python

import requests
import json
import csv
import time
import urllib3
from decouple import config
from hurry.filesize import size
from prettytable import PrettyTable

# Disable Security warning
urllib3.disable_warnings()


# Global variables

realm = "pam"
user = config('username')
password = config('password')
username = user + "@" + realm
credential = {"username":username, "password":password }

# File Inventory


def hosts(filename):
    PORT = 8006
    HOST = []
    with open (filename, "r") as f:
        lines = f.readlines()
        for link in lines :
            link = link.splitlines()
            HOST.append(link)
            url = "https://%s:%s" %(HOST,PORT)
            return url
    

def auth(url):
    url1= url + "/api2/json/access/ticket" 
    response = requests.post(url1, data=credential, verify=False)
    data = json.loads(response.text.encode('utf8'))
    data2 = json.dump(data, open("data2.json", "w"), sort_keys=True, indent=4)
    if not response.ok:
        raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))

    ticket = data['data']['ticket']
    crsf = data['data']['CSRFPreventionToken']
    clustername = data['data']['clustername']

    return ticket, crsf, clustername
   


#main program
hosts('/home/khalis/lab-temp/python-lab/proxmox-script/inventory.txt')
auth(url)
