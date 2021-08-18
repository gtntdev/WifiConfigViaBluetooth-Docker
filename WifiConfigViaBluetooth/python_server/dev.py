#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
#sys.path.append('/usr/local/lib/python2.7/dist-packages')
from bluetooth import *
import subprocess
import time
#sys.path.append('/home/pi/.local/lib/python2.7/site-packages')
from wifi import Cell, Scheme
import json

wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"

class Network:
    def __init__(self, ssid):
        self.ssid = ssid
    def dump(self):
        return {"ssid": self.ssid}

def wifi_scan():
    Cells = Cell.all('wlan0')
    wifi_info = ''
    CellsList = list(Cells)
    for current in range(len(CellsList)):
        wifi_info +=  CellsList[current].ssid + "\n"
        network_list = wifi_info.splitlines()
    #print (network_list)
    net = []
    for i in network_list:
        network = Network(i)
        net.append(network)
    #print(net)
    json_string = json.dumps([o.dump() for o in net])
    print ("Scanned wifis: " + json_string)
    return json_string

def wifi_set(ssid, psk):
    # write wifi config to file
    f = open('wpa.conf', 'w')
    f.write('country=DE\n')
    f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    f.write('update_config=1\n')
    f.write('\n')
    f.write('\n')
    f.close()

    cmd = 'mv wpa.conf ' + wpa_supplicant_conf
    cmd_result = ""
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))

    cmd = 'wpa_passphrase \'' + ssid + '\' \'' + psk + '\' >> ' + wpa_supplicant_conf
    cmd_result = ""
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))

    # restart wifi adapter
    cmd = 'wpa_cli -i wlan0 reconfigure'
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))

    time.sleep(20)

    p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = p.communicate()

    ip_address = "<Not Set>"

    for l in out.split(b'\n'):
        if l.strip().startswith(b"inet "):
#            print l
            ip_address = l.strip().split(b' ')[1]

    return ip_address

def handle_client(client_sock) :
    received_str = client_sock.recv(1024).decode('utf-8')
    if received_str == '' :
        return

    print ("received text")
    rec_str = json.loads(received_str)
    print (rec_str)
    print (rec_str["command"])

    if rec_str["command"] == "WIFI_SCAN" :
        result = wifi_scan()
        client_sock.send(result + "|")
      # return
# The previous "return" may cause an early stop of this function

    if rec_str["command"] == "WIFI_SET" :
        ssid = rec_str["ssid"]
        password = rec_str["password"]
        print ("received ssid: "+ ssid + ", password: " + password)
        result = wifi_set(ssid, password)
        client_sock.send(result.decode('utf-8') + "|")
        return


    return

try:
    while True:
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        uuid = "815425a5-bfac-47bf-9321-c5ff980b5e11"

        advertise_service( server_sock, "RPi Wifi config",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ])


        print (f"Waiting for connection on RFCOMM channel {port}")

        client_sock, client_info = server_sock.accept()
        print ("Accepted connection from ", client_info)

        handle_client(client_sock)

        client_sock.close()
        server_sock.close()

        # finished config
        print ('Socket closed\n')


except (KeyboardInterrupt, SystemExit):
    print ('\nExiting\n')
