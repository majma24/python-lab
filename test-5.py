#!/usr/bin/env python

import requests
import argparse
import getpass
import urllib3
import json 

#Disable Security warning
urllib3.disable_warnings()

class url:
    def __init__(self):
        self.url = "https://192.168.226.35:8006/api2/json/access/ticket"

class proxmoxauth:
    def login(self, cookie, csrf, realm="pam"):
        user = input("Username >>> ")
        username = user + "@" + realm
        password = getpass.getpass()
        credential = {"username":username, "password":password } 
        response = requests.post(self.url, verify=False, data=credential) 
        data = response.json()
        #return {'ticket': data['data']['ticket'], 'crsf': data['data']['CSRFPreventionToken']}
        ticket = data['data']['ticket']
        csrf = data['data']['CSRFPreventionToken']
        return ticket, csrf
        

class proxmox():
    def __init__(self, auth):
        self.url = "https://192.168.226.35:8006/api2/json/access"
        self.cookie = {'PVEAuthCookie':str(auth['ticket'])}
        self.httpheaders = {
            'Accept: */*'
            'Content-Type: application/json;charset=UTF-8'
            'Connection: keep-alive'
            'CSRFPreventionToken':str(auth['crsf'])
        }
    def vmlist(self, vm):
        self.url = self.url + "cluster/resources?type=%s" % vm
        response = requests.get(self.url, cookies = self.cookie, headers = self.httpheaders)
        res = response.json()
        data = res['data']['node']['vmid']['name']['maxcpu']['maxmem']['status']
        print(data)
















