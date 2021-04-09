#!/usr/bin/env python


filename = open("Inventory", "r")
#iplist = []
for line in filename.readlines():
    data = line.rstrip("\n")
    
    print (data)


    