#!/bin/bash

cn=$1
cnpid=$(docker inspect $cn | grep '"Pid"' | awk '{ print $2 }' | sed 's/,.*//' )
echo "Now create netns ${cn} based on Pid=${cnpid}"
touch /var/run/netns/${cn}
echo "ln -sf /proc/${cnpid}/ns/net /var/run/netns/${cn}"
ln -sf /proc/$cnpid/ns/net /var/run/netns/$cn
