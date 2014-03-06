#!/usr/bin/python

import fileinput
from bisect import bisect_left 

def analyze_retrans(pkt_lst):
    in_cnt = dict()
    in_time = dict()
    
    out_lst = list()
    out_time = dict()

    flow = pkt_lst[0][0]
    for pkt in pkt_lst:
        d, f, seq, ack, time = pkt[2], pkt[3], int(pkt[4]), int(pkt[5]), float(pkt[7])

        if 'R' in f or 'F' in f:
            break
        if 'S' in f:
            seq += 1

        if d == 'IN':
            in_cnt[ack] = in_cnt.get(ack, 0) + 1
            in_time[ack] = time
        else:
            if len(out_lst) == 0 or out_lst[-1] < seq:
                out_lst.append(seq)
                out_time[seq] = time
                continue
            else:
                # cause of sampling, find the nearest sequence number
                pos = bisect_left(out_lst, seq)
                retrans = time - out_time[out_lst[pos]]

                # determine whether it's fast retrans or timeout retrans
                print flow, seq, retrans, in_cnt.get(seq, 0), time-in_time.get(seq, time+1)

                # update out info
                if out_lst[pos] != seq:
                    out_lst.insert(pos, seq)
                out_time[seq] = time

lst = list()
for line in fileinput.input():
    lst.append(line.strip().split())

analyze_retrans(lst)
