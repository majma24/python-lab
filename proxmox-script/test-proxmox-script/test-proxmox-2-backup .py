#!/usr/bin/env python

import requests
import json
import csv
import os
import urllib3
from decouple import config
from hurry.filesize import size
from prettytable import PrettyTable

# Disable Security warning
urllib3.disable_warnings()

# Define HOST, Credential user
HOST = input("HOST : ")
PORT = 8006
realm = "pam"
url = "https://%s:%s" %(HOST,PORT)

user = config('username')
password = config('password')

username = user + "@" + realm
credential = {"username":username, "password":password }
print("\n")

    

# Generate Token
url1= url +"/api2/json/access/ticket" 
response = requests.post(url1, data=credential, verify=False)

if response.status_code == 200:
    
    print("OK, respon status : ", response.status_code, "\n")
    print("---- Generate Token and Cookie -----\n")
    print("Ticket >>> DONE \n")
    print("Token  >>> DONE \n")
else :
    print ("Error, respon status : ", response.status_code)
data = json.loads(response.text.encode('utf8'))
ticket = data['data']['ticket']
crsf = data['data']['CSRFPreventionToken']
print("---- Generate Token and Cookie -----\n")
print("Ticket >>> DONE \n")
print("Token  >>> DONE \n")

# Get Node Proxmox

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


# Get list item
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


#commit



# Save Node File To Local
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

#save VM List File to local
fname = "../proxmox-script/list-vm.csv"
with open(fname, "w") as file:
    vm_file = csv.writer(file, delimiter="\t")
    vm_file.writerow(["Node","Hostname","VMID","CPU","Memory","Disk","Status"])
    for vm in r_datavm["data"]:
        vm_file.writerow([vm["node"],vm["name"],vm["vmid"],vm["maxcpu"],size(vm["maxmem"]),size(vm["maxdisk"]),vm['status']])
    print("Save file to CSV ==> DONE \n")

list_vm = PrettyTable()
list_vm.field_names= ["Node","Hostname","VMID","CPU","Memory","Disk","Status"]
list_vm.align["Hostname"] = "l"
for vm in r_datavm['data']:
    data_vm = ([vm["node"],vm["name"],vm["vmid"],vm["maxcpu"],size(vm["maxmem"]),size(vm["maxdisk"]),vm['status']]) 
    list_vm.add_row(data_vm)
fprint = open("../proxmox-script/Readme.md", "a")
print(list_vm.get_string(sortby="Node"), file=fprint)
print("\n")


    
        

    