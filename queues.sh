#!/bin/bash

# Delete all QoS and queues

sudo ovs-vsctl -- clear Port s1-eth1 qos
sudo ovs-vsctl -- clear Port s3-eth1 qos
sudo ovs-vsctl -- clear Port s2-eth1 qos -- clear Port s2-eth2 qos
sudo ovs-vsctl -- --all destroy QoS -- --all destroy Queue

# Create new ones

echo "SWITCH 1"
# First switch
sudo ovs-vsctl set port s1-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000 \
queues=1=@1q,3=@3q -- \
--id=@1q create queue other-config:min-rate=1000 other-config:max-rate=$1 -- \
--id=@3q create queue other-config:min-rate=1000 other-config:max-rate=$3

# Second switch
echo "SWITCH 2"
# First port
sudo ovs-vsctl set port s2-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000 \
queues=1=@1q,3=@3q -- \
--id=@1q create queue other-config:min-rate=1000 other-config:max-rate=$1 -- \
--id=@3q create queue other-config:min-rate=1000 other-config:max-rate=$3


# Second port
sudo ovs-vsctl set port s2-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000 \
queues=2=@2q,3=@3q -- \
--id=@2q create queue other-config:min-rate=1000 other-config:max-rate=$2 -- \
--id=@3q create queue other-config:min-rate=1000 other-config:max-rate=$3

# Third switch
echo "SWITCH 3"
# Second port
sudo ovs-vsctl set port s3-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000 \
queues=2=@2q,3=@3q -- \
--id=@2q create queue other-config:min-rate=1000 other-config:max-rate=$2 -- \
--id=@3q create queue other-config:min-rate=1000 other-config:max-rate=$3
