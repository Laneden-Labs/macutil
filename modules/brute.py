#!/bin/bash/python3

import random
import subprocess
import time
import re
import sys
import os
from .general import get_file_content
from .utility import interface_down, interface_up, check_user


def get_local_address(interface):	
	# Check relevant interface for DHCP assigned address
	process = subprocess.Popen('ifconfig {interface}'.format(interface=interface), shell=True, stdout=subprocess.PIPE)
	output = process.communicate()[0]
	lines = output.splitlines()
	for line in lines:
		match = re.match(b'.*\s(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s.*', line)
		if match:
			# Return an identified IP address
			return(match.group(1))
		
	# Return None if no address found
	return None
	

def chunk_me(mac_address):
	# Randomly assign last 3 octets of MAC address and return a completed vendor address
	mac_2 = (":%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),))
	mac = mac_address + mac_2.upper()
	return mac


def mac_search(mac_list, interface):
	
	if check_user():
		random.shuffle(mac_list)
		# For each MAC address in our Vendor List
		print('\nSpoofing Mac Addresses\n')
		for mac in mac_list:
			
			# Create a valid random address from the vendor supplied MAC address
			mac_address = chunk_me(mac[0])
			interface_down(interface)
			time.sleep(2)
			interface_up(interface)
			
			# Alter our system MAC address to that of the newly generated vendor mac address
			process = subprocess.Popen('ifconfig {interface} ether {mac_address}'.format(interface=interface, mac_address=mac_address), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
			output = process.communicate()[0]
			interface_up(interface)
			print('Set:\t{}\t{}'.format(mac_address, mac[1]))
			time.sleep(15)
			
			# Check if DHCP assigned us an ip address based on our spoofed MAC address
			result = get_local_address(interface)
			if result:
				if not result.startswith(b'169'):
					print('\nValid MAC Address Identified:\n')
					print('\tInterface:\t{}'.format(interface))
					print('\tIp:\t\t{}'.format(result.decode()))
					print('\tVendor:\t\t{}'.format(mac[1]))
					print('\tMac:\t\t{}\n'.format(mac_address))
					sys.exit()


# MAIN
# Start the MAC address search
def start(interface):
	# A List of common Telephone Vendor Mac Addresses
	filename = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + '/doc/known_macs.txt')
	mac_list = get_file_content(filename)
	
	# Start Bruting
	mac_search(mac_list, interface)