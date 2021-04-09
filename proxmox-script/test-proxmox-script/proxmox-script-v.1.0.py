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

# Clear File 

with open("Readme.md","r+") as fp:
  fp.truncate(0)
  fp.close()

with open("../proxmox-script/List-VM.md", "r+") as fp2:
    fp2.truncate(0)
    fp2.close()

# Global Username 
realm = "pam"
user = config('username')
password = config('password')
username = user + "@" + realm
credential = {"username":username, "password":password }

filename = "inventory.txt"
PORT = 8006

with open(filename, 'r') as fp:
    for count, ip in enumerate(fp):
        ip = ip.strip()
        url = "https://"+ip+":"+str(PORT)

        # Generate Token

        url1= url +"/api2/json/access/ticket" 
        response = requests.post(url1, data=credential, verify=False)
        data = json.loads(response.text.encode('utf8'))
        data2 = json.dump(data, open("../proxmox-script/data_json/data" + "-" + str(ip)+ ".json", "w"), sort_keys=True, indent=4)
        if not response.ok:
            raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))
          
        ticket = data['data']['ticket']
        crsf = data['data']['CSRFPreventionToken']
        clustername = data['data']['clustername']
        print("clustername : ", clustername)
        print("======================================================")
        print("|               PROXMOX RESOURCE                     |")
        print("======================================================")    
        print("(-) Generate Token ==> Done")

        #Get Node Proxmox

        url2 = url + "/api2/json/cluster/resources?type=node" 
        #url2 = url  + "/api2/json/nodes"
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
        r_nodes2 = json.dump(r_nodes, open("../proxmox-script/data_json/node_cluster-"+ clustername+".json", "w"), sort_keys=True, indent=4)

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
        datavm = json.dump(r_datavm, open("../proxmox-script/data_json/vm_cluster-"+ clustername+".json", "w"), sort_keys=True, indent=4)

        # Get Info Storage
        url4 = url +"/api2/json/cluster/resources?type=storage"
        cookie = {'PVEAuthCookie' : ticket}
        header = {
            'Accept': '*/*',
            'Content-Type' :'application/json',
            'CSRFPreventionToken': str(crsf) 
        }
        disk = requests.get(url4, cookies = cookie, headers= header, verify=False)
        disks = disk.json()
        r_disk = json.dumps(disks, sort_keys=True, indent=4)
        r_disks = json.loads(r_disk)
        storage = json.dump(r_disks, open("../proxmox-script/data_json/storage-"+ clustername+".json", "w"), sort_keys=True, indent=4)

        
        #Save Node File To Local

        fprint = open("../proxmox-script/Readme.md", "a")
        print("# Proxmox Resource", file=fprint)
        print("\n")
        
        print("### Proxmox Cluster" + " " + clustername + " " + "Node", file=fprint)
        print("|   Hostname   | Total-CPU | Total-Memory | Total Disk | CPU Usage(%) | RAM Usage |", file=fprint)
        print("|   :------:   |  :------: | :------: | :------: | :------: | :------: |", file=fprint)
        for nodes in r_nodes['data']:
            print("|" + " " +nodes["node"] + " " + "|" + "  " + str(nodes["maxcpu"]) + " " + "|" + " " + str(size(nodes["maxmem"])) + " " + "|" 
                    + " " + str(size(nodes["maxdisk"])) + " " + "|" + " " + str(round((nodes['cpu'])*100, 2)) + " " + "|" + " "+ str(size(nodes["mem"])) + " " + "|", file=fprint)

        
        print("(-) Save List Node To Readme.md ==> DONE \n")

        # Commit Changes

        
        
        
        #Save VM List File to local
        
        fprint1 = open("../proxmox-script/List-VM.md", "a")
        
        print('### Proxmox Cluster' + ' ' +  clustername +  ' '  + 'List VM', file=fprint1)
        print("|     Node     |     Hostname    |   VMID   | CPU Allocate | Memory Allocate | Disk Allocate | Status |", file=fprint1)
        print("|  :------:    |     :------:    | :------: | :------: | :------: | :------: | :------: |", file=fprint1)
        for vm in r_datavm['data']:
            print("|" + " " + vm["node"] + " " + "|" + " " + vm["name"] + " " + "|" + " " + str(vm["vmid"]) + " " + "|" + " " + str(vm["maxcpu"]) + " " + "|" 
                    + " " +  str(size(vm["maxmem"]))+ " " + "|" + " " + str(size(vm["maxdisk"]))+ " " + "|" + " " + vm['status'] + " " + "|", file=fprint1)

            
        print("(-) Save VM List To .md File ==> DONE \n")
        
            




        

