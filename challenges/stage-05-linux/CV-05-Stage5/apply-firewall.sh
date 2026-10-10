#!/bin/bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "Run this script with sudo." >&2
    exit 1
fi

running=$(docker inspect --format '{{.State.Running}}' cybervault-cv05-cv05-1)
if [[ "$running" != "false" ]]; then
    echo "Stop CV-05 before applying firewall rules." >&2
    exit 1
fi

iptables -S DOCKER-USER >/dev/null

prepare_chain() {
    local tool="$1" chain="$2"
    if ! "$tool" -S "$chain" >/dev/null 2>&1; then
        "$tool" -N "$chain"
    fi
    "$tool" -F "$chain"
}

attach_first() {
    local tool="$1" parent="$2" chain="$3"
    while "$tool" -C "$parent" -j "$chain" >/dev/null 2>&1; do
        "$tool" -D "$parent" -j "$chain"
    done
    "$tool" -I "$parent" 1 -j "$chain"
}

prepare_chain iptables CV05-INPUT
iptables -A CV05-INPUT -i br-cv05 \
    -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
iptables -A CV05-INPUT -i br-cv05 -j DROP
iptables -A CV05-INPUT -i enp0s3 \
    -s 192.168.60.100/32 -d 192.168.60.50/32 \
    -p tcp --dport 2222 -j ACCEPT
iptables -A CV05-INPUT -p tcp --dport 2222 -j DROP
iptables -A CV05-INPUT -j RETURN

prepare_chain iptables CV05-FORWARD
iptables -A CV05-FORWARD \
    -i enp0s3 -o br-cv05 \
    -s 192.168.60.100/32 -d 172.30.50.10/32 \
    -p tcp --dport 22 \
    -m conntrack --ctstate NEW,ESTABLISHED --ctdir ORIGINAL \
    --ctorigdst 192.168.60.50 --ctorigdstport 2222 -j ACCEPT
iptables -A CV05-FORWARD \
    -i br-cv05 -o enp0s3 \
    -s 172.30.50.10/32 -d 192.168.60.100/32 \
    -p tcp --sport 22 \
    -m conntrack --ctstate ESTABLISHED --ctdir REPLY \
    --ctorigsrc 192.168.60.100 \
    --ctorigdst 192.168.60.50 --ctorigdstport 2222 -j ACCEPT
iptables -A CV05-FORWARD -i br-cv05 -j DROP
iptables -A CV05-FORWARD -o br-cv05 -j DROP
iptables -A CV05-FORWARD -j RETURN

prepare_chain ip6tables CV05-INPUT6
ip6tables -A CV05-INPUT6 -i br-cv05 -j DROP
ip6tables -A CV05-INPUT6 -p tcp --dport 2222 -j DROP
ip6tables -A CV05-INPUT6 -j RETURN

prepare_chain ip6tables CV05-FORWARD6
ip6tables -A CV05-FORWARD6 -i br-cv05 -j DROP
ip6tables -A CV05-FORWARD6 -o br-cv05 -j DROP
ip6tables -A CV05-FORWARD6 -j RETURN

attach_first iptables INPUT CV05-INPUT
attach_first iptables DOCKER-USER CV05-FORWARD
attach_first ip6tables INPUT CV05-INPUT6
attach_first ip6tables FORWARD CV05-FORWARD6

echo "CV-05 IPv4 and IPv6 firewall rules applied."
