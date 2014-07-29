#### Install python Nmap module http://xael.org/norman/python/python-nmap/
####
####
####
####
#### Usage: ./enumerate.py <ip address>
####
####

#!/bin/python
import sys
import os
import subprocess
import nmap
import time
import ftplib
import shlex

print "Looking for low hanging fruit hang on..."
time.sleep(20)
print "Still lookin, patience young padewan..."

IP = sys.argv[1] # IP address
os.system("mkdir /root/Desktop/"+IP) # Creates a directory on your Desktop
nm = nmap.PortScanner() # Initialize Nmap module
nm.scan(IP, '80,443,22,21,139,445') # Target ports
nm.command_line()
nm.scaninfo()

###########################
def ftp(): # Attempts to login to FTP using anonymous user
	try:
		ftp = ftplib.FTP(IP)
		ftp.login()
		print "\o/"
		print "FTP ALLOWS ANONYMOUS ACCESS!"
		print "o/\o"
		print "*" * 10
		ftp.quit()
	except:
		print "FTP does not allow anonymous access :("
############################

############################
def dirb(): # Runs dirb on http pages.
	os.system('xterm -hold -e dirb http://'+IP+' -o /root/Desktop/'+IP+'/dirb_info.txt &')
	print 'Running Dirb on port 80 - Check the folder for output file.'
############################

###########################
def dirb_https(): # Runs dirb on https pages.
	os.system('xterm -hold -e dirb https://'+IP+' -o /root/Desktop/'+IP+'/dirb_https_info.txt &')
	print 'Running Dirb on port 443 - Check the folder for output file.'
###########################

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

# Function Checks
if nm[host].has_tcp(21) and nm[IP]['tcp'][21]['state'] == 'open':
	print "*" * 10
	print "FTP FOUND - CHECKING FOR ANONYMOUS ACCESS"
	ftp()
if nm[host].has_tcp(80) and nm[IP]['tcp'][80]['state'] == 'open':
	dirb()
if nm[host].has_tcp(443) and nm[IP]['tcp'][443]['state'] == 'open':
	dirb_https()

#Nmap Service Scan
print "#" * 10
print "Beginning Service Scan of all ports... Your pwnage can begin soon..."
print "#" * 10
os.system("nmap -sV -p- -v -T4 -oN /root/Desktop/"+IP+"/service_scan.txt "+IP) # Full TCP scan of all 65535 ports
