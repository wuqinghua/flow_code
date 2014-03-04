#!/usr/bin/python

import sys
from bisect import bisect_left

def handle_list(lst):
    in_list = list()
    in_time_list = list()
    out_list = list()
    out_time_list = list()

    send_rate_list = list()
    recv_rate_list = list()
    rtt_list = list()
    retrans_list = list()

    base_time = float(lst[0][7])
    for _ in lst:
        d = _[2]
        t = float(_[7]) - base_time
        if d == 'IN':
            ack = int(_[5])
            if len(in_list) > 0:
                if ack < in_list[-1]:
                    # XXX the two ack packets are disordered
                    # print 'ack sequence error', ack, in_list[-1]
                    # sys.exit()
                    pass
                elif ack == in_list[-1]:
                    # retransmission of ack packet
                    retrans_list.append((d, t))
                else: 
                    # get recv rate
                    recv_rate_list.append((ack-in_list[-1], t-in_time_list[-1]))

                    # find the acked data in out_list
                    p = bisect_left(out_list, ack)
                    if p < len(out_list) and out_list[p] == ack:
                        rtt_list.append(t-out_time_list[p])

            in_list.append(ack)
            in_time_list.append(t)

        elif d == 'OUT':
            seq = int(_[4])
            if len(out_list) > 0:
                if seq <= out_list[-1]:
                    # retransmission of data packet
                    retrans_list.append((d, t))
                else:
                    # get sending rate
                    send_rate_list.append((seq-out_list[-1], t-out_time_list[-1]))

            out_list.append(seq)
            out_time_list.append(t)

    data = out_list[-1]-out_list[0]
    time = out_time_list[-1]-out_time_list[0]

    print data, time 
    print 'send: '
    for _ in send_rate_list:
        print '%d:%.6f' % (_[0], _[1]),
    print '\nrecv: '
    for _ in recv_rate_list:
        print '%d:%.6f' % (_[0], _[1]),
    print '\nretrans: '
    for _ in retrans_list:
        print '%3s:%.6f' % (_[0], _[1]),
    print '\nRTT: '
    for _ in rtt_list:
        print '%.6f' % (_), 
    print '\n'

if len(sys.argv) == 1:
    ifile = open('clean_flows.txt')
else:
    ifile = open(sys.argv[1])

while True:
    line = ifile.readline()
    if line == '':
        break

    lst = list()
    num = int(line)
    for _ in range(num):
        line = ifile.readline()
        lst.append(tuple([ _ for _ in line.strip().split() ]))

    handle_list(lst)
