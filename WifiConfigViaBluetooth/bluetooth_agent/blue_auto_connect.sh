#!/usr/bin/expect -f
set prompt "#"
spawn bluetoothctl

expect -re $prompt
send "default-agent\r"
sleep 2

expect -re $prompt
send "agent NoInputNoOutput\r"
sleep 2

expect -re $prompt
send "power on\r"
sleep 2

expect -re $prompt
send "pairable on\r"
sleep 2

expect -re $prompt
send "discoverable on\r"
sleep 2

set timeout 60
expect "Confirm passkey"
sleep 2
send "yes\r"

set timeout 2
expect -re $prompt
sleep 2

send "quit\r"

interact

