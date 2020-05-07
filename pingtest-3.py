#!/usr/bin/env python

import os
import platform
result_files = open("hasil_ping.txt" , "w")
with open("list_ip.txt" , "r") as files:
   iplist = files.read().splitlines()
   print(iplist)
   

for ip in iplist:
    response = os.system("ping " + ("-n 1 " if platform.system().lower()=="windows" else "-c 1 ") + ip)
    if response == 0:
        #status = ip + "Server is UP"
        print(ip, "is UP")
        result_files.writelines(f"{ip} is UP \n")
    else:
        #status = ip + "Server is Down"
        print(ip, "is DOWN")
        result_files.writelines(f"{ip} is DOWN \n") 



