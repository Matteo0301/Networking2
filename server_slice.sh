#!/bin/bash

add_slice1(){
    remove_slice2
    # First switch
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:1,normal
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:1,normal
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:1,normal


    # Second switch
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.2,idle_timeout=0,actions=set_queue:1,normal
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.3,idle_timeout=0,actions=set_queue:1,normal
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.4,idle_timeout=0,actions=set_queue:1,normal
}

remove_slice1(){
    # First switch
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.10,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.10,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

    # Second switch
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.3,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.4,idle_timeout=0,actions=drop
}

add_slice2(){
    remove_slice1
    # Third switch
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:2,normal
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:2,normal
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:2,normal
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.10,idle_timeout=0,actions=set_queue:2,normal

    # Second switch
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.6,idle_timeout=0,actions=set_queue:2,normal
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.7,idle_timeout=0,actions=set_queue:2,normal
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.8,idle_timeout=0,actions=set_queue:2,normal
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.9,idle_timeout=0,actions=set_queue:2,normal
}

remove_slice2(){
    # Third switch
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.10,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.10,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.10,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

    # Second switch
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.6,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.8,idle_timeout=0,actions=drop
    sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
}

case $1 in
    add1) add_slice1
    ;;
    add2) add_slice2
    ;;
    remove1) remove_slice1
    ;;
    remove2) remove_slice2
    ;;
    *) echo "error"
    exit 1
    ;;
esac