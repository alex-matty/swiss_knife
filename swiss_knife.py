#!/usr/bin/python3

##############################################################
# Created by @meganuke_ -------------------------------------#
# This script can be used, modify, replicate for any purpose #
# without any restrictions. ---------------------------------#
# Version: 0.3 ----------------------------------------------#
##############################################################

# Import required libraries
# Import argparse to get the arguments from the terminal instead of input or fixed variables
import argparse
# Get date and time for printing formats 
from datetime import datetime
# Import socket to attempt connections with other systems
import socket
# Import OS to perform the ping scans
import os

# ANSI Escape sequence codes are in octal mode '[ is a control sequence introducer'
# Using a class to be able to reuse it for other color purposes (Review the usage of classes and their implementation)
class terminal_output_colors:
    yellow_color = '\033[33m'
    green_color = '\033[32m'
    reset_color = '\033[0m'
    bold_style = '\033[1m'
    red_background_color = '\033[41m'

# Create a help menu and the arguments to pass to create a better UI and UX
parser = argparse.ArgumentParser(
    prog='Swiss Kinfe',
    description='Script will first perform a ping scan to know if the target host is up, if they are it will perform a port scan; otherwise it will exit when acknowledging that the target host is down. For the time being it scans all 65535 ports',
    epilog='Created by @meganuke_')
parser.add_argument('-t', '--ipaddress', help='target IP address(es) to scan')
parser.add_argument('-pn', '--pingscan', help='Disable port scan, perform a ping scan only', action='store_true')
parser.add_argument('-ps', '--portscan' , help='Disable ping scan, perform only a port scan', action='store_true')
args = parser.parse_args()

# Get the IP(s) the user provided
ip_address = args.ipaddress
pingscan = args.pingscan
portscan = args.portscan

# If the user provides comma separated IPs put them in the list
if ',' in ip_address:
    ip_address = ip_address.split(',')

# Function to perform a ping scan (add the option to add more IPs)
def ping_scan(ips):
    # Create a sweet output with the target IP and port
    if type(ips) is str:
        print('\n')
        print(terminal_output_colors.bold_style + 'Ping Scan' + terminal_output_colors.reset_color)
        print(terminal_output_colors.green_color + '-' * 50)
        print('scanning:' + ips)
        print('Scan started at: ' + str(datetime.now()))
        print('-' * 50 +'\n' + terminal_output_colors.reset_color)

        # Logic to perform the ping scan to verify if a host is alive
        hostname = ips
        command = 'ping ' + hostname + ' -c 2 1>/dev/null'
        returned_value = os.system(command)
        if returned_value == 0:
            print(terminal_output_colors.yellow_color + hostname + ' is up' + terminal_output_colors.reset_color + '\n')
        else:
            print(terminal_output_colors.yellow_color + hostname + ' is down' + terminal_output_colors.reset_color + '\n')
            exit()
    elif type(ips) is list:
        print('\n')        
        print(terminal_output_colors.bold_style + 'Ping Scan' + terminal_output_colors.reset_color)
        print(terminal_output_colors.green_color + '-' * 50)
        print('scanning:' + str(ips))
        print('Scan started at: ' + str(datetime.now()))
        print('-' * 50 +'\n' + terminal_output_colors.reset_color)
        for ip in ips:
            # Logic to perform the ping scan to verify if a host is alive
            hostname = ip
            command = 'ping ' + hostname + ' -c 2 1>/dev/null'
            returned_value = os.system(command)
            if returned_value == 0:
                print(terminal_output_colors.yellow_color + hostname + ' is up' + terminal_output_colors.reset_color)
            else:
                print(terminal_output_colors.yellow_color + hostname + ' is down' + terminal_output_colors.reset_color)

# Function to perform a TCP port scan (add the option to add more IPs and select ports to scan and the option to select it using the terminal as a flag)
def port_scan(ips):
    # Create a sweet output with the target IP and port
    if type(ips) is str:
        print('\n')        
        print(terminal_output_colors.bold_style + 'TCP Port Scan' + terminal_output_colors.reset_color)
        print(terminal_output_colors.green_color + '-' * 50)
        print('scanning:' + ips)
        print('Scan started at: ' + str(datetime.now()))
        print('-' * 50 +'\n' + terminal_output_colors.reset_color)

        # Logic to scan ports (Turn it into a function)
        for port in range(1,65535):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # Return closed port indicator
            result = s.connect_ex((ips, port))
            if result == 0:
                print(terminal_output_colors.yellow_color + 'Port {} is open'.format(port) + terminal_output_colors.reset_color)
            s.close()
    # Create a sweet output with the target IP and port
    if type(ips) is list:
        print('\n')        
        print(terminal_output_colors.bold_style + 'TCP Port Scan' + terminal_output_colors.reset_color)
        print(terminal_output_colors.green_color + '-' * 50)
        print('scanning: ' + str(ips))
        print('Scan started at: ' + str(datetime.now()))
        print('-' * 50 +'\n' + terminal_output_colors.reset_color)
        for ip in ips:
            # Logic to scan ports (Turn it into a function)
            print(ip)
            for port in range(1,65535):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)

                # Return closed port indicator
                result = s.connect_ex((ip, port))
                if result == 0:
                    print(terminal_output_colors.yellow_color + 'Port {} is open'.format(port) + terminal_output_colors.reset_color)
                s.close()

# Start the functions (add options to select which one(s) to pick)
if args.pingscan:
    ping_scan(ip_address)
    exit()
elif args.portscan:
    port_scan(ip_address)
    exit()
else:
    ping_scan(ip_address)
    port_scan(ip_address)