#!/usr/bin/env python

List_ip = open("list_ip.txt" , "r")
iplist = List_ip.read().splitlines()
iplist.append("yahoo.com")
print (f"{iplist} \n")
print(iplist[0])