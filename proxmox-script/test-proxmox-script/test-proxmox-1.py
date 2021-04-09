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

        #Save Node File To Local
        #nodefile = "../proxmox-script/list-node.csv"
        #with open(nodefile, "w") as file:
        #    node_file = csv.writer(file, delimiter="\t")
        #    node_file.writerow(["Hostname","Total-CPU","Total-Memory","Total Disk","CPU Usage (%)","RAM Usage"])
#
        #    for nodes in r_nodes["data"]:
        #        node_file.writerow([nodes["node"],nodes["maxcpu"],size(nodes["maxmem"]),size(nodes["maxdisk"]), round((nodes['cpu'])*100, 2),size(nodes['mem'])])


        list_node = PrettyTable()
        list_node.title = 'Proxmox Cluster' + ' ' +  clustername  +  ''  + 'Node'
        list_node.field_names= ["Hostname","Total-CPU","Total-Memory","Total Disk","CPU Usage(%)","RAM Usage"]
        for nodes in r_nodes['data']:
            data_node = ([nodes["node"],nodes["maxcpu"],size(nodes["maxmem"]),size(nodes["maxdisk"]),round((nodes['cpu'])*100, 2),size(nodes["mem"])])
            list_node.add_row(data_node) 
        fprint = open("../proxmox-script/Readme.md", "w")
        print(list_node.get_string(sortby="Hostname"), file=fprint)

        #save VM List File to local
        #fname = "../proxmox-script/list-vm.csv"
        #with open(fname, "w") as file:
        #    vm_file = csv.writer(file, delimiter="\t")
        #    vm_file.writerow(["Node","Hostname","VMID","CPU","Memory","Disk","Status"])
        #    for vm in r_datavm["data"]:
        #        vm_file.writerow([vm["node"],vm["name"],vm["vmid"],vm["maxcpu"],size(vm["maxmem"]),size(vm["maxdisk"]),vm['status']])
        #    print("(-) Save file to CSV ==> DONE \n")

        list_vm = PrettyTable()
        list_vm.title = 'Proxmox Cluster' + ' ' +  clustername +  ''  + 'List VM'
        list_vm.field_names= ["Node","Hostname","VMID","CPU","Memory","Disk","Status"]
        list_vm.align["Hostname"] = "l"
        for vm in r_datavm['data']:
            data_vm = ([vm["node"],vm["name"],vm["vmid"],vm["maxcpu"],size(vm["maxmem"]),size(vm["maxdisk"]),vm['status']]) 
            list_vm.add_row(data_vm)
        fprint = open("../proxmox-script/Readme.md", "a")
        print(list_vm.get_string(sortby="Node"), file=fprint)
        print("(-) Save File To Readme.md ==> DONE \n")
        print("\n")

