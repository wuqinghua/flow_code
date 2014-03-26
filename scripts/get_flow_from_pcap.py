#!/usr/bin/python

import sys

flow = sys.argv[1]
b, e = None, None

for line in open('../flow_data/20140319_pcap_flow_index.txt'):
    t = line.strip().split()

    if t[0] == flow:
        b, e = int(t[1]), int(t[2])

ifile = open('../flow_data/20140319_pcap_sorted.pcap', 'rb')
hdr = ifile.read(24)
ifile.seek(b, 0)
cont = ifile.read(e-b)
ifile.close()

ofile = open(flow + '.pcap', 'wb')
ofile.write(hdr)
ofile.write(cont)
ofile.close()
