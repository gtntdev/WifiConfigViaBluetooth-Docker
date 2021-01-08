This project aims to provide functionality to configure (scan, connect and
in the future more options will be added likely) the Wifi connection of a 
Raspberry Pi over Bluetooth remotely with an Android app.

It's based on this project: https://github.com/brendan-myers/rpi3-wifi-conf
but further development brought it to a whole new level: I migrated the server
script into a docker container which is based on a debian image.
Because of the portability of docker this docker build guide should be easily
applicable to all unix-like operating systems (only small mods needed).

Please have a look at the Wiki page to get started.
https://github.com/gtntdev/-WifiConfigViaBluetooth-Docker/wiki

As needed resources (Bluetooth/Wifi) depend on the specific host, changes to the 
source code could be necessary when deployed on other machines then the RPi.

Please make sure your are connected to the host over ethernet since existing
Wifi connection will fail during setup process.

How it works:
```
                           java                                     Network                                       python
                                                               -----------------
Command object --> Json Object --> Json String --> Bytes    -->       Bytes     -->      Bytes --> Json String --> Json Object --> Command Object
...                                                                                                                                           ...
...                                                                                                                                           ... 
Command object <-- Json Object <-- Json String <-- Bytes    <--       Bytes     <--      Bytes <-- Json String <-- Json Object <-- Command Object
                                                               -----------------

----Commands----
Client:
	> is Wifi connected :           'boolean'
        App: [button (red = not connected, yellow = querrying device for status, 
		green = connected, display information, grey = not bt device selected)] (not implemented yet)
	> get wifi connection :         'Wifi Object' (not implemented yet)
	App: 
	> scan for available networks : 'List of wifi object' (already implemented)
	> set wifi connection:          'boolean' (success?) (already implemented)
Server:
	> later: network state changed


[TODO]
- CRUD Operations for Wifi Networks stored persistent -> Wifi Network Class -> DB Connection Manager
Wifi Network Class:
    > Static List of Wifi
	> SSID (network Name)
	> Password
	> MAC Address (primary key in db)
```
