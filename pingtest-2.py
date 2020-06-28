#!/user/bin/env python

import subprocess

iplist = open("list_ip.txt" , "r")

for ip in iplist:
#    output = os.popen(f"ping{ip}").read()
    status,output = subprocess.getstatusoutput(f"ping -c1 {str(ip)}")
    if  status == 0:
        print(f"{ip} is UP \n")
    else:
        print(f"{ip} is DOWN \n")