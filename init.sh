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


./queues.sh 4000 5000 2000