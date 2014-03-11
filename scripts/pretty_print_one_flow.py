#!/usr/bin/python

import fileinput

in_seq = 0
in_ack = 0
time = -1

for line in fileinput.input():
    pkt = line.strip().split()

    if time == -1:
        time = float(pkt[7])

    if pkt[2] == 'OUT':
        if in_seq == 0:
            in_seq = int(pkt[5])
        if in_ack == 0:
            in_ack = int(pkt[4])
        print '%3.6f %s %d %d %s %s' % (float(pkt[7])-time, pkt[2], int(pkt[4])-in_ack, int(pkt[5])-in_seq, pkt[3], pkt[6])
    else:
        if in_seq == 0:
            in_seq = int(pkt[4])
        if in_ack == 0:
            in_ack = int(pkt[5])
        print '%3.6f %s %d %d %s %s' % (float(pkt[7])-time, pkt[2], int(pkt[4])-in_seq, int(pkt[5])-in_ack, pkt[3], pkt[6])
