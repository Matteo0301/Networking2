#!/bin/bash

start(){
    # Add flows
    # First switch
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.5,idle_timeout=0,actions=set_queue:3,normal

    # Third switch
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.1,idle_timeout=0,actions=set_queue:3,normal
}

stop(){
    # Remove flows
    # First switch
    sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.5,idle_timeout=0,actions=drop

    # Third switch
    sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
}

case $1 in
    start) start
    ;;
    stop) stop
    ;;
    *) echo "error"
    exit 1
    ;;
esac