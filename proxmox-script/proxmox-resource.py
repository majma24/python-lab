#!/usr/bin/env python3

import requests
import json
import os
import urllib3
from hurry.filesize import size


# Disable Security warning
urllib3.disable_warnings()

# Clear File 

with open("../Proxmox_Python_Script/Readme.md","r+") as fp:
  fp.truncate(0)
  fp.close()

# Global Username 
realm = "pam"
user = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
username = str(user) + "@" + "pam"
credential = {"username":username, "password":password }
print("\n")

filename = "../Proxmox_Python_Script/inventory.txt"
PORT = 8006

with open(filename, 'r') as fp:
    for count, ip in enumerate(fp):
        ip = ip.strip()
        url = "https://"+ip+":"+str(PORT)

        # Generate Token

        url1= url +"/api2/json/access/ticket" 
        response = requests.post(url1, data=credential, verify=False)
        data = json.loads(response.text.encode('utf8'))
        
        if not response.ok:
            raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))
          
        ticket = data['data']['ticket']
        crsf = data['data']['CSRFPreventionToken']
        clustername = data['data']['clustername']
        print("clustername : ", clustername)
        print("======================================================")
        print("|               PROXMOX RESOURCE SCRIPT               |")
        print("======================================================")    
        print("(-) Generate Token ==> Done")

        #Get Node Proxmox

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
        r_nodes2 = json.dump(r_nodes, open("../Proxmox_Python_Script/data_json/node_cluster-"+ clustername+".json", "w"), sort_keys=True, indent=4)

        # Get list vm item
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
        datavm = json.dump(r_datavm, open("../Proxmox_Python_Script/data_json/vm_cluster-"+ clustername+".json", "w"), sort_keys=True, indent=4)

        # Node Proxmox
        
        fprint = open("../Proxmox_Python_Script/Readme.md", "a")
        print("\n")
        print("### Proxmox Cluster" + " " + clustername + " " + "Node", file=fprint)
        print("|   Hostname   | Total-CPU | Total-Memory | Total Disk | CPU Usage (%) | RAM Usage |", file=fprint)
        print("|     :------:   |  :------: | :------: | :------: | :------: | :------: |", file=fprint)
        for nodes in r_nodes['data']:
            print("|" + " " +str(nodes["node"]) + " " + "|" + "  " + str(nodes["maxcpu"]) + " " + "|" + " " + str(size(nodes["maxmem"])) + " " + "|" 
                    + " " + str(size(nodes["maxdisk"])) + " " + "|" + " " + str(round((nodes['cpu'])*100, 2)) + " " + "|" + " "+ str(size(nodes["mem"])) + " " + "|", file=fprint)

        
        print("(-) Save List Node To Readme.md ==> DONE")


	# List VM

        fprint = open("../Proxmox_Python_Script/Readme.md", "a")

        print('### Proxmox Cluster' + ' ' +  clustername +  ' '  + 'List VM', file=fprint)
        print("|       Node     |       Hostname    |   VMID   | CPU Allocate | Memory Allocate | Disk Allocate | Status |", file=fprint)
        print("|     :------:     |      :------:     | :------: |    :------:    |    :------:    |    :------:    | :------: |", file=fprint)
        for vm in r_datavm['data']:
            print("|" + " " + str(vm["node"]) + " " + "|" + " " + str(vm["name"]) + " " + "|" + " " + str(vm["vmid"]) + " " + "|" + " " + str(vm["maxcpu"]) + " " + "|" 
                    + " " +  str(size(vm["maxmem"]))+ " " + "|" + " " + str(size(vm["maxdisk"]))+ " " + "|" + " " + vm['status'] + " " + "|", file=fprint)

        print("(-) Save List VM To Readme.md ==> DONE")
        print("\n")


