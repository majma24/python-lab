#!/usr/bin/env python

import requests
import os
import time
import json
import csv
import urllib3
from decouple import config
from hurry.filesize import size
from prettytable import PrettyTable

# Disable Security warning
urllib3.disable_warnings()

# Global Username 
realm = "pam"
user = config('username')
password = config('password')
username = user + "@" + realm
credential = {"username":username, "password":password }
print("\n")


def load_file(fname):
    fname = "../inventory.txt"
    data = []
    with open(fname, 'r') as f:
        data = f.read().splitlines()
        f.close
    return data


def run_job(data):
    HOST = data
    PORT = 8006
    url = "https://%s:%s" %(HOST,PORT)

    
def auth(url):
    url1= url +"/api2/json/access/ticket" 
    response = requests.post(url1, data=credential, verify=False)
    data = json.loads(response.text.encode('utf8'))
    if not response.ok:
      raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))   
    ticket = data['data']['ticket']
    crsf = data['data']['CSRFPreventionToken']
    clustername = data['data']['clustername']

    print(ticket)
    print(crsf)
    print(clustername)

auth('url1')