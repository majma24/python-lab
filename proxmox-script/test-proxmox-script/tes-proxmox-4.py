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
    data = []
    with open(fname, 'r') as f:
        data = f.read().splitlines()
        f.close
    return data


def run_job(ip):
    HOST = ip
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

def node(url, ticket, crsf, clustername):
    url2 = url + "/api2/json/cluster/resources?type=node" 
    cookie = {'PVEAuthCookie' : ticket}
    header = {
        'Accept': '*/*',
        'Content-Type' :'application/json',
        'CSRFPreventionToken': str(crsf)  
    }

    node = requests.get(url2, cookies = cookie, verify=False)	
    raw_node = node.json()
    r_node = json.dumps(raw_node, indent=4, sort_keys=True)
    r_nodes = json.loads(r_node)

    nodefile = "../proxmox-script/list-node.csv"
    with open(nodefile, "w") as file:
        node_file = csv.writer(file, delimiter="\t")
        node_file.writerow(["Hostname","Total-CPU","Total-Memory","Total Disk","CPU Usage (%)","RAM Usage"])
       
    for nodes in r_nodes["data"]:
        node_file.writerow([nodes["node"],nodes["maxcpu"],size(nodes["maxmem"]),size(nodes["maxdisk"]), round((nodes['cpu'])*100, 2),size(nodes['mem'])])
     
    list_node = PrettyTable()
    list_node.field_names= ["Hostname","Total-CPU","Total-Memory","Total Disk","CPU Usage(%)","RAM Usage"]
    for nodes in r_nodes['data']:
        data_node = ([nodes["node"],nodes["maxcpu"],size(nodes["maxmem"]),size(nodes["maxdisk"]),round((nodes['cpu'])*100, 2),size(nodes["mem"])])
        list_node.add_row(data_node) 
    fprint = open("../proxmox-script/Readme.md", "w")
    print(list_node.get_string(sortby="Hostname"), file=fprint)


def list_vm(url, ticket, crsf):
    url3 = url + "/api2/json/cluster/resources?type=vm" 

    cookie = {'PVEAuthCookie' : ticket}
    header = {
        'Accept': '*/*',
        'Content-Type' :'application/json',
        'CSRFPreventionToken': str(crsf) 
    }
    result = requests.get(url3, cookies = cookie, headers= header, verify=False)
    data = result.json()
    r_data = json.dumps(data, indent=4, sort_keys=True)
    r_datavm = json.loads(r_data)

    filename = "../proxmox-script/list-vm.csv"
    with open(filename, "w") as file:
        vm_file = csv.writer(file, delimiter="\t")
        vm_file.writerow(["Node","Hostname","VMID","CPU","Memory","Disk","Status"])
    for vm in r_datavm["data"]:
        vm_file.writerow([vm["node"],vm["name"],vm["vmid"],vm["maxcpu"],size(vm["maxmem"]),size(vm["maxdisk"]),vm['status']])
    print("(-) Save file to CSV ==> DONE \n")

    list_vm = PrettyTable()
    list_vm.field_names= ["Node","Hostname","VMID","CPU","Memory","Disk","Status"]
    list_vm.align["Hostname"] = "l"
    for vm in r_datavm['data']:
        data_vm = ([vm["node"],vm["name"],vm["vmid"],vm["maxcpu"],size(vm["maxmem"]),size(vm["maxdisk"]),vm['status']]) 
        list_vm.add_row(data_vm)
    fprint = open("../proxmox-script/Readme.md", "w")
    print(list_vm.get_string(sortby="Node"), file=fprint)
    print("\n")

def execute_job():
    list_ip = load_file('inventory.txt')
    for ip in list_ip:
        run_job(ip, auth, list_vm, node)
        time.sleep(1)
    time.sleep(1)
    print("ALL DONE")


# Main 
execute_job()