# Build this from Ubuntu 22.04
FROM ubuntu:22.04
# start getting needed packages
RUN apt update
RUN apt install python3 -y
RUN apt install net-tools -y
RUN apt install inetutils-ping -y
RUN apt install iproute2 -y
RUN apt install openssh-server sudo -y
RUN apt install iptables -y
RUN apt install dnsmasq -y
RUN apt install python3-flask -y

EXPOSE 0

WORKDIR /app
COPY files/optional.txt /app/data.txt
COPY files/source.py /app/main.py

CMD ["python3", "main.py"]