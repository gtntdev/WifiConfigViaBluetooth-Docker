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
