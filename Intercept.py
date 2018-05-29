#!/usr/bin/python

import socket
import sys

from IPv4 import IPv4
from TCP import TCP
from HTTP import HTTP
from struct import *
from io import StringIO

TAB_1 = '\t '
TAB_2 = '\t\t '
TAB_3 = '\t\t\t '

HTTP_PORT = 80
MAX_PORTS = 65535

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


try:
    # Create the socket
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
except error:
    print(bcolors.FAIL + 'Socket could not be created.' + bcolors.ENDC)
    sys.exit()

while True:
    # Accept a tcp packet
    packet, addr = s.recvfrom(MAX_PORTS)

    raw_data = packet[14:]
    ipv4 = IPv4(raw_data)
    tcp = TCP(ipv4.data)

    if (len(tcp.data) > 0):
        # For checking HTTP data
        http = HTTP(tcp.data)
        if tcp.src_port == HTTP_PORT or tcp.dest_port == HTTP_PORT:
            print(bcolors.OKGREEN + TAB_1 + 'TCP Segment:' + bcolors.ENDC)
            print(bcolors.OKGREEN + TAB_2 + 'Source Addr: {} {}, \n {}Destination Addr: {} {}'.format(TAB_2, ipv4.src, TAB_2, TAB_1, ipv4.target))
            print(bcolors.OKGREEN + TAB_2 + 'Source Port: {} {}, \n {}Destination Port: {} {}'.format(TAB_2, tcp.src_port, TAB_2, TAB_1, tcp.dest_port) + bcolors.ENDC)
            print(bcolors.OKGREEN + TAB_2 + 'Sequence: {} {}, \n {}Acknowledgment: {} {} \n'.format(TAB_2, tcp.sequence, TAB_2, TAB_1, tcp.acknowledgment) + bcolors.ENDC)
            try:
                if isinstance(http.data, str):
                    print(bcolors.HEADER + 'HTTP Data:' + bcolors.ENDC)
                    buf = StringIO(http.data)
                    print(buf.read())
                else:
                    print(bcolors.HEADER + 'HTTP Data:' + bcolors.ENDC)
                    buf = StringIO(http.data.decode('utf-8'))
                    print(http.data)

            except Exception as e:
                print(bcolors.FAIL + str(e) + bcolors.ENDC)