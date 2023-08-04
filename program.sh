#!/bin/sh

ryu-manager controller.py &
sleep 2
sudo python3 topology.py

sudo mn -c