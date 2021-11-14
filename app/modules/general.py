import csv
import re
import sys


# Validate Mac address
def validate_mac(mac):
	valid = re.match("[0-9A-F]{2}([-:]?)[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$", mac.upper())
	if valid:
		return True
	else:
		print('\nNot a valid MAC address: {}!\n'.format(mac))
		sys.exit()	


# Read file into list of tuples
def get_file_content(filename):
	
	known_macs = [tuple(row) for row in csv.reader(open(filename, 'r'))]
	return known_macs


# Print banner and description
def banner():
	
	title = """
	                    _   _ _ 
 _ __ ___   __ _  ___ _   _| |_(_) |
| '_ ` _ \ / _` |/ __| | | | __| | |
| | | | | | (_| | (__| |_| | |_| | |
|_| |_| |_|\__,_|\___|\__,_|\__|_|_|
 """

	banner_desc = """{bypass} | {brute} | {random}
	
{name} | {twit}
  
{url}""" . format (name="Author: Darryl Lane", twit="Twitter: @darryllane101", bypass="NAC Bypass", brute="MAC Brute Force", random="MAC Random", url="https://github.com/Laneden-Labs/macutil")

	print(title)
	print(banner_desc)	
	return


# Print full description
def full_description():
	
	content = """
 Network Access Control solutions are a simple idea, 802.1X cert based 
 authentication, great! works like a charm. However, businesses are complex 
 beasts and not all systems on that network support 802.1X and/or cert based 
 authenticaiton.
 
 In this situation most look to simple MAC authentication to handle the
 exceptions. 
 
 So if lets say your IP phones are on the same network, if we can find the
 correct MAC address we can essential spoof that address and access the network.

 This utility was designed for exactly this, MAC address manipulation and brute
 forcing.

optional arguments:
  -h, --help            Show this help message and exit
  -v                    Display current version
  -vendor               Select a vendor to spoof
  -list-vendor          List all vendors available in system
  -set                  Set specific MAC address "Required: -mac, -interface"
  -mac                  Address required for "Required: -set"
  -brute                Brute force a MAC address, NAC bypassing
  -random               Set a random MAC address
  -list                 List current interfaces on the system
  -reset                Reset MAC address to default
  -interface            Interface to be manipulated
  """
	
	print(content)
	return


# Print usage menu and examples
def description():
	
	content = """
optional arguments:
  -h, --help            Show this help message and exit
  -v                    Display current version
  -vendor               Select a vendor to spoof
  -list-vendor          List all vendors available in system
  -set                  Set specific MAC address "Required: -mac, -interface"
  -mac                  Address required for "Required: -set"
  -brute                Brute force a MAC address, NAC bypassing
  -random               Set a random MAC address
  -list                 List current interfaces on the system
  -reset                Reset MAC address to default
  -interface            Interface to be manipulated
  
examples:

macutil -brute
macutil -brute -interface en4
macutil -set -mac 00:11:22:33:44:55 -interface en0
macutil -reset -interface en0
"""
	print(content)
	return
