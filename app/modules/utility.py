import random
import subprocess
import re
import sys
import os
from .general import get_file_content


# Check if user is running as root/sudo
def check_user():
	if os.getuid() == 0:
		return True
	else:
		print('\nroot required!...')	
		sys.exit()


#interface down
def interface_down(interface):
	if check_user:
		subprocess.Popen('ifconfig {interface} down'.format(interface=interface), shell=True, stdout=subprocess.PIPE)
	return


#interface up
def interface_up(interface):
	if check_user:
		subprocess.Popen('ifconfig {interface} up'.format(interface=interface), shell=True, stdout=subprocess.PIPE)	
	return


# Randomly generate MAC address and return
def random_generator():
	mac = ("%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	return mac.upper()


# Request interface details
def request_interfaces(args):
	live = []
	results = re.findall(r'^(?:Hardware Port|Device|Ethernet Address): (.+)$',
	                     subprocess.check_output(('networksetup', '-listallhardwareports'), 
	                                             universal_newlines=True), re.MULTILINE)	
	
	for i in range(0, len(results), 3):
		# Split results
		port, device, address = results[i:i + 3]
		if args['list']:
			print('\tPort:\t\t{}\n\tInterface:\t{}\n\tMac:\t\t{}\n'.format(port,device, address))
		
		process = subprocess.Popen("ifconfig {}".format(device), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		# Identify live ipv4 interfaces
		output = process.communicate()[0].decode()
		lines = output.splitlines()		
		for line in lines:
			if re.match(r'.*inet\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\snetmask\s(.*)\sbroadcast\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\.*', line):
				live_ip = re.match(r'.*inet\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\snetmask\s(.*)\sbroadcast\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\.*', line).group(1)
				live.append('port: {port}'.format(port=port))
				live.append('interface: {inter}'.format(inter=device))
				live.append('mac: {mac}'.format(mac=address))
				live.append('ip: {ipadd}'.format(ipadd=live_ip))				
	
	# Return dictionary of live results
	return {"live": [dict(item.split(": ") for item in live)]}	


# A List of common Telephone Vendor Mac Addresses
def get_vendors(args):
	vendor_list = []
	vendor_spoof = []
	filename = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + '/doc/known_macs.txt')
	mac_list = get_file_content(filename)
	
	for item in mac_list:
		if args['vendor']:
			vendor_select = args['vendor']
		else:
			vendor_select = None
			
		if '-' in item[1]:
			vendor = item[1].strip().rstrip().split('-')[0]
		else:
			vendor = item[1].strip().rstrip()
		
		if vendor_select:
			if vendor.capitalize() == vendor_select.capitalize():
				vendor_list.append(vendor)
				vendor_spoof.append(item)
		else:					
			vendor_list.append(vendor)
			vendor_spoof.append(item)
			
	vendor_list = sorted(set(sorted(vendor_list)))
	
	if args['list_vendor']:
		print('\nVendors:\n')
		for item in vendor_list:
			print('\t{}'.format(item))
		sys.exit()
	else:
		return vendor_spoof


# List all interfaces
def list_interfaces(args):
	print('\nAll Interfaces\n')
	
	# Execute and parse interface output into list
	live_interfaces = request_interfaces(args)
	
	for k, v in live_interfaces.items():
		for value in v:
			print('Live Interfaces:\n')
			print('\tPort:\t\t{port}'.format(port=value['port']))
			print('\tInterface:\t{inter}'.format(inter=value['interface']))
			print('\tMac:\t\t{mac}'.format(mac=value['mac']))
			print('\tIP:\t\t{ipadd}\n'.format(ipadd=value['ip']))
	return


# Reset interface MAC address to default
def reset_default_mac(args, interface):
	
	results = re.findall(r'^(?:Hardware Port|Device|Ethernet Address): (.+)$',
	                     subprocess.check_output(('networksetup', '-listallhardwareports'), 
	                    universal_newlines=True), re.MULTILINE)
	
	for i in range(0, len(results), 3):
		port, interface, address = results[i:i + 3]
		if port == 'Bluetooth PAN':
			pass
		else:	
			if args['interface']:
				interface = args['interface']
				
			process = subprocess.Popen("ifconfig {}".format(interface), shell=True, stdout=subprocess.PIPE)
			output = process.communicate()[0].decode()
			lines = output.splitlines()
			for line in lines:
				if interface in line:
					set_mac_address(address, interface)
					return
	return		


# Set MAC address to interface
def set_mac_address(mac_address, interface):
	check_user()
	subprocess.Popen("ifconfig {interface} ether {mac_address}".format(interface=interface, mac_address=mac_address), shell=True, stdout=subprocess.PIPE)
	print('\nSet Mac Address:\n')
	print('\tMac:\t\t{}'.format(mac_address))
	print('\tInterface:\t{}'.format(interface))
	return


# Get live interfaces
def get_live_interfaces_mac(args):
	return request_interfaces(args)
