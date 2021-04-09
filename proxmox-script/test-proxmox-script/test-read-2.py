#!/usr/bin/env python

import requests
import json
import time
from decouple import config
import urllib3

# Disable Security warning
urllib3.disable_warnings()

filename = "inventory.txt"
PORT = 8006

with open(filename, 'r') as fp:
    for count, ip in enumerate(fp):
        ip = ip.strip()
        url = "https://"+ip+":"+str(PORT)
        print(url)