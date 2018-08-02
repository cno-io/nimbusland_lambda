#!/usr/bin/python

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

import requests
from netaddr import IPNetwork, IPAddress
import json
from xml.dom import minidom

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
__website__ = 'Stage2Sec.com'
__blog__ = 'https://Stage2Sec.com/blog/'

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

'''

--- Nimbusland - AWS and Azure IP Check - Alpha v0.0.7 ---

Checks if an IP address is known to be assoicated with AWS or Azure

'''

class Nimbusland:

    def __init__(self):
        self.aws_url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
        self.azure_url = 'https://download.microsoft.com/download/0/1/8/018E208D-54F8-44CD-AA26-CD7BC9524A8C/PublicIPs_20180730.xml'
        self.aws_ips = {}
        self.azure_ips = {}

        self._load_aws_ips()
        self._load_azure_ips()

    def _load_aws_ips(self):
        self.aws_ips = json.loads(requests.get(self.aws_url, allow_redirects=True, verify=False).content)

    def _load_azure_ips(self):
        self.azure_ips = minidom.parseString(requests.get(self.azure_url, allow_redirects=True, verify=False).content.decode("utf-8")).getElementsByTagName('Region')

    def get_aws_ip_info(self, target_ip):
        for item in self.aws_ips["prefixes"]:
            if IPAddress(target_ip) in IPNetwork(str(item["ip_prefix"])):
                return [target_ip, str(item["ip_prefix"]), str(item["region"]), 'AWS', str(item["service"])]

        return False

    def get_azure_ip_info(self, target_ip):
        for s in self.azure_ips:
            region_name = str(s.attributes['Name'].value)
            ilist = s.getElementsByTagName('IpRange')
            for r in ilist:
                cidr = str(r.attributes['Subnet'].value)
                if IPAddress(target_ip) in IPNetwork(cidr):
                    return [target_ip, cidr, str(region_name), 'Azure', "Microsoft"]

        return False