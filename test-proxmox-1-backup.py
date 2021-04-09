#!/usr/bin/env python

import requests
import json
import csv
import getpass
import urllib3
from hurry.filesize import size
from prettytable import PrettyTable

# Disable Security warning
urllib3.disable_warnings()

# Define HOST, Credential user
HOST = input("HOST : ")
PORT = 8006
realm = "pam"
url = "https://%s:%s" %(HOST,PORT)

user = input("username : ")
username = user + "@" + realm
password = getpass.getpass()
credential = {"username":username, "password":password }
print('\n')
# Generate Token
url1= url +"/api2/json/access/ticket" 
response = requests.post(url1, data=credential, verify=False)

if response.status_code == 200:
    data = json.loads(response.text.encode('utf8'))
    ticket = data['data']['ticket']
    crsf = data['data']['CSRFPreventionToken']
    print("OK, respon status : ", response.status_code, "\n")
    print("---- Generate Token and Cookie -----\n")
    print("Ticket >>> DONE \n")
    print("Token  >>> DONE \n")
else :
    print ("Error, respon status : ", response.status_code)

# Get list item
url2 = url + "/api2/json/cluster/resources?type=vm" 

cookie = {'PVEAuthCookie' : ticket}
header = {
    'Accept': '*/*',
    'Content-Type' :'application/json',
    'CSRFPreventionToken': str(crsf) 
}

result = requests.get(url2, cookies = cookie, headers= header, verify=False)
data = result.json()
r_data = json.dumps(data, indent=4, sort_keys=True)
r_data1 = json.loads(r_data)

#Print out List
list_vm = PrettyTable()
list_vm.field_names= ["Node","Hostname","VMID","CPU","Memory","Disk","Status"]
for item in r_data1['data']:
    data_vm = ([item["node"],item["name"],item["vmid"],item["maxcpu"],size(item["maxmem"]),size(item["maxdisk"]),item['status']])
    list_vm.add_row(data_vm) 
fprint = open("Readme.md", "w")
print(list_vm, file=fprint, sorted=True)

print("\n")

#save File to CSV
fname = "list-vm.csv"
with open(fname, "w") as file:
    vm_file = csv.writer(file, delimiter="\t")
    vm_file.writerow(["Node","Hostname","VMID","CPU","Memory","Disk","Status"])
    for item in r_data1["data"]:
        vm_file.writerow([item["node"],item["name"],item["vmid"],item["maxcpu"],size(item["maxmem"]),size(item["maxdisk"]),item['status']])
    print("Save file to CSV ==> DONE \n")

# Get Node Proxmox

# Get Node Proxmox

#url3 = url + "/api2/json/cluster/resources?type=node" 
url3 = url + "/api2/json/nodes"

cookie = {'PVEAuthCookie' : ticket}
header = {
    'Accept: */*',
    'Content-Type :application/json',
    'CSRFPreventionToken: str(crsf)' 
}

node = requests.get(url3, cookies = cookie, verify=False)
raw_node = node.json()
outfile = open('node.json','w')
json_nodes = json.dumps(raw_node, indent=4, sort_keys=True)
json_nodes1 = json.dump(raw_node,outfile,indent=4, sort_keys=True)
r_nodes = json.loads(json_nodes)

for node in r_nodes['data']:
    nodename = node['node']
    nodecpu = node['maxcpu']
    nodemem = size(node['maxmem'])
    nodedisk = size(node['maxdisk'])

if nodename == item["node"] :
    memoryused = size(sum(item['maxmem'] for item in r_data1['data']))
    cpuused = sum(item['maxcpu'] for item in r_data1['data'])
print(memoryused)
print(cpuused)




    
    




    
        

    