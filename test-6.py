#!/usr/bin/env python

import requests
import json
import urllib3
import getpass

urllib3.disable_warnings()

host = input("Hosts : ")
port = 8006
url = "https://%s:%s"

user = input("Username : ")
realm = "pam"
username = user + "@" + realm
password = getpass.getpass()
credential = {"Username" :username, "Password" :password}


def getticket(ticket, csrf):
    url2 = url + "/api2/json/access/ticket"
    response = requests.post(url2, verify=False, data=credential)
    res_json = json.loads(response.text)
    ticket = res_json["data"]["ticket"]
    token = res_json["data"]["CSRFPreventionToken"]
    return ticket, csrf

def getVMS():
    url3 = url + "/api2/json/cluster/resources?type=vm"
    
    cookie = {'PVEAuthCookie': getticket(ticket='ticket')}
    header = {
      'Accept: */*'
      'Content-Type: application/json'
      'Connection: keep-alive'
      'CSRFPreventionToken : str(token)'
    }

    respond = requests.get(url3, verify=False, cookies=cookie)
    result = respond.json()
    
    






    




