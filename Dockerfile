FROM debian:buster

RUN apt-get update
RUN apt-get -y install nano
RUN apt-get -y install expect
RUN apt-get -y install python3
RUN apt-get -y install wpasupplicant
RUN apt-get -y install bluetooth libbluetooth-dev

RUN apt-get -y install python3-pip

RUN pip3 install wifi
RUN pip3 install python-wifi
RUN pip3 install pybluez

RUN apt-get -y install wireless-tools
RUN apt-get -y install net-tools

COPY WifiConfigViaBluetooth /WifiConfigViaBluetooth
COPY wpa.conf /etc/wpa_supplicant/wpa_supplicant.conf
 
#helper
#ps aux
RUN apt-get -y install procps
RUN apt-get install -y strace

#main script PID 1
CMD /bin/bash /start.sh
