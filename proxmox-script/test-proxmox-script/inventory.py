#!/usr/bin/env python

import os

inventory = ("/home/khalis/lab-temp/python-lab/proxmox-script/inventory")

inv = os.listdir(inventory)

for node in inv :
    data = open(node, 'r')
print(data)