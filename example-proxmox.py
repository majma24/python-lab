#!/usr/bin/env python

import argparse
import requests
import sys
import getpass

# Proxmox Constants
PROXMOX_HOST = "<CLUSTER NAME>"  # can also be an IP or the FQDN of the host
PROXMOX_PORT = 8006

# Disable security warnings not reccomended
requests.packages.urllib3.disable_warnings()

# Authentication class
class ProxmoxAuth:
    def __init__(self):
      self.url = "https://%s:%s/api2/json/access/ticket" % (PROXMOX_HOST, PROXMOX_PORT)

    def login(self, realm="pam"):
      user = raw_input("Username [%s]: " % getpass.getuser())
      if not user:
        user = getpass.getuser()
      user = user + "@" + realm
      
      password = getpass.getpass()
      credentials = { "username":user, "password":password }
      response = requests.post(self.url,verify=False,data=credentials)
      if not response.ok:
          raise AssertionError('Authentification Error: HTTP Result: \n {}'.format(response))

      data = response.json()
      return {'ticket': data['data']['ticket'], 'crsf': data['data']['CSRFPreventionToken']}

class Proxmox():
    def __init__(self, auth):
      self.baseurl = "https://%s:%s/api2/json/" % (PROXMOX_HOST, PROXMOX_PORT)
      self.cookie = {'PVEAuthCookie':auth['ticket']}
      # Setup HTTP headers
      self.httpheaders = {
        'Accept':'application/json',
        'Content-Type':'application/x-www-form-urlencoded',
        'CSRFPreventionToken':str(auth['crsf'])
        }

    def migrate_host(self, node, target, vmid):
      """ Migrate the virutal machine with id <vmid> from the node to the target """
      fullurl = self.baseurl + "nodes/%s/qemu/%s/migrate" % (node,vmid)
      data = {'target': str(target), 'online': str(1)} # always use online mode
      response = requests.post(
        fullurl, 
        verify=False, 
        data = data,
        cookies = self.cookie,
        headers = self.httpheaders)
      if not response.ok:
          raise AssertionError('Error moving VM: HTTP Result: \n {}'.format(response))
      return True

    def migrate_hosts(self, node, target, vmids):
      """ Migrate the listed virutal machines from the node to the target """
      for vmid in vmids:
        self.migrate_host(node, target, vmid)

def main():
  """ Get's valid login creditinals and migrates the virutal machines """
  parser = argparse.ArgumentParser(description='Proxmox Migration Helper')
  parser.add_argument('-n','--node', help="Node ID of machine currently hosting the virtual machines", required=True)
  parser.add_argument('-t','--target', help="Node ID of target machine to migrate to", required=True)
  parser.add_argument('vmids', type=int, nargs='+', help='List of VM IDs to migrate')
  args = parser.parse_args()
  # Login to cluster
  auth = ProxmoxAuth().login()
  api = Proxmox(auth)
  # Do the migration
  api.migrate_hosts(args.node, args.target, args.vmids)

if __name__ == "__main__":
    main()