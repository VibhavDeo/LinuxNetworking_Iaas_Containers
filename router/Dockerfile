# Build this from Ubuntu 22.04
FROM ubuntu:22.04
# start getting needed packages
RUN apt update
RUN apt install net-tools -y
RUN apt install inetutils-ping -y
RUN apt install iproute2 -y
RUN apt install openssh-server sudo -y
RUN apt install iptables -y
RUN apt install dnsmasq -y
# Here we just run something in the foreground so container won't exit...
CMD tail -f /dev/null
