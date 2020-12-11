#!/bin/bash

until ! /WifiConfigViaBluetooth/bluetooth_agent/blue_auto_connect.sh
do
    echo 3
done

exit 0

