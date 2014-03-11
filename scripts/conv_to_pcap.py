#!/usr/bin/python

import fileinput
from socket import inet_aton
from struct import pack, unpack

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

def update_cs(ip_hdr):
    cs = pack("H", checksum(ip_hdr))
    lst = list(ip_hdr)
    lst[10] = cs[0]
    lst[11] = cs[1]
    return ''.join(lst)

def flags(msg):
    dic = { 'F':0, 'S':1, 'R':2, 'P':3, '.':4 }
    i = 0
    for _ in msg:
        i |= 1 << dic[_]
    return i


eth1 = '\x44\x37\xe6\x04\x05\x06'
eth2 = '\x38\x22\xd6\x01\x02\x03'

def conv_to_pcap(pkt):
    if pkt[2] == 'IN':
        src_eth = eth1
        src_ip = '.'.join(pkt[0].split('.')[:4])
        src_port = int(pkt[0].split('.')[4])
        dst_eth = eth2
        dst_ip = '.'.join(pkt[1].split('.')[:4])
        dst_port = int(pkt[1].split('.')[4])
    else:
        dst_eth = eth1
        dst_ip = '.'.join(pkt[0].split('.')[:4])
        dst_port = int(pkt[0].split('.')[4])
        src_eth = eth2
        src_ip = '.'.join(pkt[1].split('.')[:4])
        src_port = int(pkt[1].split('.')[4])
    
    flag = flags(pkt[3])
    seq, ack = int(pkt[4]), int(pkt[5])
    length = int(pkt[6])
    sec = int(pkt[7].split('.')[0])
    usec = int(pkt[7].split('.')[1])
    wind = int(pkt[9])
    
    ip_len = 40 + length
    pkt_len = 14 + ip_len
    cap_len = 54
    
    pkt_hdr = pack('IIII', sec, usec, cap_len, pkt_len)

    eth_hdr = pack('!6s6sH', src_eth, dst_eth, 0x0800)
    
    ip1 = unpack("!L", inet_aton(src_ip))[0]
    ip2 = unpack("!L", inet_aton(dst_ip))[0]
    ip_hdr = pack('!BBHHHBBHII', 0x45, 0x00, ip_len, 0, 0, 64, 0x06, 0x00, ip1, ip2)
    ip_hdr = update_cs(ip_hdr)

    tcp_hdr = pack('!HHIIHHHH', src_port, dst_port, seq, ack, 0x05 << 12 | flag, wind, 0, 0)

    return pkt_hdr + eth_hdr + ip_hdr + tcp_hdr

fheader = pack('IHHIIII', 0xA1B2C3D4, 0x0002, 0x0004, 0, 0, 0xFFFF, 0x01)

ofile = open('flow.pcap', 'w')

# write file header
ofile.write(fheader)

for _ in fileinput.input():
    # write each packet
    items = _.strip().split()
    if len(items) < 13:
        continue

    pkt = conv_to_pcap(items)
    ofile.write(pkt)

ofile.close()
