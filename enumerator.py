#!/usr/bin/python
""" Author: Maleus
    Usage:  ./enumerator.py <ip>
    Date:   7.28.14
    Made for Kali Linux, not tested on other distros.
"""

import sys
import os
import nmap
import ftplib
import subprocess

if len(sys.argv) != 2:	
	print "Usage ./enumerator.py <ip>"
	sys.exit(1)
IP = sys.argv[1] # IP address
HOME = os.environ['HOME'] # Sets environment variable for output directory to the current users 'Home' folder.
OUTPUT_DIRECTORY = os.path.join(HOME, "Desktop", IP)# Sets path for folder on users desktop named as the IP address being scanned
try:
	os.makedirs(OUTPUT_DIRECTORY)# Creates folder on users Desktop
except:
	CUSTOM_NAME = raw_input("IP directory already exists; Please enter the name of your loot directory: ")
	OUTPUT_DIRECTORY = os.path.join(HOME, "Desktop", CUSTOM_NAME)
	os.makedirs(OUTPUT_DIRECTORY)

print "Lookin for easy pickins... Hang tight."
nm = nmap.PortScanner() # Initialize Nmap module
nm.scan(IP, '80,443,22,21,139,445') # Target ports

def ftp(): # Attempts to login to FTP using anonymous user
	try:
		ftp = ftplib.FTP(IP)
		ftp.login()
		print "0.0"
		print "FTP ALLOWS ANONYMOUS ACCESS!"
		ftp.quit()
	except:
		print "FTP does not allow anonymous access :("

def dirb_80(): # Runs dirb on port 80.
	DIRB_80 = os.path.join(OUTPUT_DIRECTORY, 'dirb_80.txt')
	os.system('xterm -hold -e  dirb http://'+IP+' -o '+DIRB_80+' &')
	print 'Running Dirb on port 80 - Check the target folder for output file.'

def dirb_443(): # Runs dirb on port 443.
	DIRB_443 = os.path.join(OUTPUT_DIRECTORY, 'dirb_443.txt')
	os.system('xterm -hold -e dirb https://'+IP+' -o ' +DIRB_443+ ' &')
	print 'Running Dirb on port 443 - Check the target folder for output file.'

def enum4linux(): # Runs enum4linux on the target machine if smb service is detected.
	ENUM_FILE = os.path.join(OUTPUT_DIRECTORY, 'enum_info.txt')
	proc = subprocess.Popen('enum4linux '+IP+' > '+ENUM_FILE+' &', shell = True)
	stdout,stderr = proc.communicate()
	print 'Beginning enum4linux - this may take a few minutes to complete. - Info will be available in the enum_info.txt file -'
	

def nikto_80(): # Runs Nikto on port 80
	NIKTO_80 = os.path.join(OUTPUT_DIRECTORY, 'nikto_80.txt')
	os.system('xterm -hold -e nikto -host http://'+IP+' -output '+NIKTO_80+' &')
	print 'Running Nikto against port 80 - Check target folder for output file.'

def nikto_443():# Runs Nikto on port 443
	NIKTO_443 = os.path.join(OUTPUT_DIRECTORY, 'nikto_443.txt')
	os.system('xterm -hold -e nikto -host https://'+IP+' -output '+NIKTO_443+' &')
	print 'Running Nikto against port 443 - Check target folder for output file.'

#Initial Nmap scans
for host in nm.all_hosts():
	print('--------------------')
	print('Host: %s (%s)' % (IP, nm[host].hostname()))
	print('State: %s' % nm[host].state())
	print('--------------------')

for proto in nm[host].all_protocols():
	print('--------------------')
	print('Protocol: %s' % proto)

lport = nm[host]['tcp'].keys()
lport.sort()
for port in lport:
	print('--------------------')
	print('port: %s\tstate: %s' % (port, nm[host][proto][port]['state']))
	print('--------------------')

def has_open_port(port_num):
	return nm[IP]['tcp'][port_num]['state'] == 'open'

#Function Checks
if has_open_port(21):
	ftp()
if has_open_port(80):
	dirb_80()
	nikto_80()
if has_open_port(443):
	dirb_443()
	nikto_443()
if has_open_port(139):
	enum4linux()
if has_open_port(445):
	enum4linux()

#Nmap Service Scan
print "Beginning Service Scan of all ports... Your pwnage can begin soon..."
NMAP_INFO = os.path.join(OUTPUT_DIRECTORY, 'nmap_full.txt')# Nmap full service info file
os.system('nmap -A -p- -T4 -oN '+NMAP_INFO+' '+IP) # Full TCP scan of all 65535 ports


