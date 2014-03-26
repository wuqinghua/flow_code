#!/usr/bin/python

import dpkt
import socket
import sys

this_ip = '101.226.161.206'

flag_dic = { 1:'F', 2:'S', 4:'R', 8:'P', 16:'.', 32:'U', 64:'E', 128:'C', 256:'N' }

def get_flags(s):
    return ''.join([ flag_dic.get(1 << i & s, '') for i in range(9) ])

f = open('../flow_data/20140319.pcap')
pcap = dpkt.pcap.Reader(f)

i = 0
for ts, buf in pcap:
    i += 1
    if i <= 17712307:
        continue

    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data

    src_ip = socket.inet_ntoa(ip.src)
    dst_ip = socket.inet_ntoa(ip.dst)

    try:
        src_port = tcp.sport
    except AttributeError:
        sys.stderr.write('%s, %s\n' % (src_ip, dst_ip))
        continue

    dst_port = tcp.dport
    seq, ack = tcp.seq, tcp.ack
    win = tcp.win
    flags = get_flags(tcp.flags)
    length = ip.len - ip.hl*4 - tcp.off*4

    if src_ip == this_ip:
        src_ip, dst_ip = dst_ip, src_ip
        src_port, dst_port = dst_port, src_port
        dir = 'OUT'
    else:
        dir = 'IN'

    # omit mss, window scale factor, col 12 and 13
    print '%s.%d' % (src_ip, src_port), '%s.%d' % (dst_ip, dst_port), dir, flags, seq, ack, length, '%.6f' % (ts), 0, win, 0, 0, 0

f.close() 
