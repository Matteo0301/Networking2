#!/bin/bash

hosts=10
set -o history -o histexpand

# Set all flows between hosts to drop packets

# First switch
attached=( 1 2 3 4 )
for src in "${attached[@]}"
do
    for dst in `seq 1 $hosts`
    do
        sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.$src,nw_dst=10.0.0.$dst,idle_timeout=0,actions=drop
    done
done

# Setting destination ports of attached hosts
for h in "${attached[@]}"
do
    sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=1,nw_dst=10.0.0.$h,idle_timeout=0,actions=output:$(($h +1)),normal
done

# Third switch
attached=( 5 6 7 8 9 )
for src in "${attached[@]}"
do
    for dst in `seq 1 $hosts`
    do
        sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.$src,nw_dst=10.0.0.$dst,idle_timeout=0,actions=drop
    done
done

for h in "${attached[@]}"
do
    sudo ovs-ofctl add-flow s3 ip,priority=65500,in_port=1,nw_dst=10.0.0.$h,idle_timeout=0,actions=output:$(($h + 1 - 4)),normal
done

# Second switch
for dst in `seq 1 $hosts`
do
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.$dst,idle_timeout=0,actions=drop
done

# Destination port of server
sudo ovs-ofctl add-flow s2 ip,priority=65500,in_port=1,nw_dst=10.0.0.10,idle_timeout=0,actions=output:3,normal
sudo ovs-ofctl add-flow s2 ip,priority=65500,in_port=2,nw_dst=10.0.0.10,idle_timeout=0,actions=output:3,normal


# Initialize queues of slice1

echo "SWITCH 1"
# First switch
sudo ovs-vsctl set port s1-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues=1=@1q,3=@3q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=2000000

# Second switch
echo "SWITCH 2"
# First port
sudo ovs-vsctl set port s2-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues=1=@1q,3=@3q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=4000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=2000000


# Second port
sudo ovs-vsctl set port s2-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues=2=@2q,3=@3q -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=2000000

# Third switch
echo "SWITCH 3"
# Second port
sudo ovs-vsctl set port s3-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues=2=@2q,3=@3q -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=2000000
