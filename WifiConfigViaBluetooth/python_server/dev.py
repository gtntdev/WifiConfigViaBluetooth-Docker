#!/usr/bin/env python

import os
import sys
#sys.path.append('/usr/local/lib/python2.7/dist-packages')
from bluetooth import *
import subprocess
import time
#sys.path.append('/home/pi/.local/lib/python2.7/site-packages')
from wifi import Cell, Scheme

#wpa_supplicant_conf = "/home/pi/Wifi\ Config\ via\ bluetooth/python_server/wpa.conf"
wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "


def wifi_connect(ssid, psk):
    # write wifi config to file
    f = open('wpa.conf', 'w')
    f.write('country=DE\n')
    f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    f.write('update_config=1\n')
    f.write('\n')
#    f.write('network={\n')
#    f.write('    ssid="' + ssid + '"\n')
#    f.write('    psk="' + psk + '"\n')
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


def ssid_discovered():
    Cells = Cell.all('wlan0')

    wifi_info = 'Found ssid : \n'

    CellsList = list(Cells)
    for current in range(len(CellsList)):
        wifi_info +=  CellsList[current].ssid + "\n"


    wifi_info+="~"

    print (wifi_info)
    return wifi_info


def handle_client(client_sock) :
    # get ssid
    client_sock.send(ssid_discovered())
    print ("Waiting for SSID...")


    ssid = client_sock.recv(1024).decode('utf-8')
    if ssid == '' :
        return

    print ("ssid received")
    print (ssid)

    # get psk
    client_sock.send("waiting-psk~")
    print ("Waiting for PSK...")


    psk = client_sock.recv(1024).decode('utf-8')
    if psk == '' :
        return

    print ("psk received")

    print (psk)

    ip_address = wifi_connect(ssid, psk)

    print ("ip address: " + ip_address.decode('utf-8'))

    client_sock.send("ip-addres:" + ip_address.decode('utf-8') + "~")

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
        print ('Finished configuration\n')


except (KeyboardInterrupt, SystemExit):
    print ('\nExiting\n')
