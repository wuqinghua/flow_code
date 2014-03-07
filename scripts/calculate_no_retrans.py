#!/usr/bin/python

import sys
from bisect import bisect_left
TOTAL_FLOW_NUMBER, REGULAR_FLOW_NUMBER = 0,0

def handle_list(lst,num):
    out_list = list()
    global REGULAR_FLOW_NUMBER
    retran = True  # just print the flow without retransmit and has been
                   # recorded fully

    for _ in lst:
        d = _[2]
        if d == 'IN':
            pass

        elif d == 'OUT':
            seq = int(_[4])
            if len(out_list) > 0:
                if seq <= out_list[-1]:
                    # retransmission of data packet
                    retran = True
                    break
                else:
                    # is not retransmit 
                    retran = False
            
            out_list.append(seq)

    if retran == False:
        REGULAR_FLOW_NUMBER +=1
        print num
        for _ in lst:
            if(len(_) == 13):
                print '%s %s %s %s %s %s %s %s %s %s %s %s %s\n' % (_[0], _[1],
                     _[2], _[3], _[4], _[5], _[6], _[7], _[8], _[9], _[10],
                    _[11], _[12]),
            else:
                print 'not 13 elements'


if len(sys.argv) == 1:
    ifile = open('/home/zhoujianer/360_flow/clean_flows.txt')
else:
    ifile = open(sys.argv[1])

while True:
    line = ifile.readline()
    TOTAL_FLOW_NUMBER +=1
    if line == '':
        print 'The total flow number is %d\n' % (TOTAL_FLOW_NUMBER -1),
        print 'The regular flow number is %d\n' % (REGULAR_FLOW_NUMBER),
        break

    lst = list()
    num = int(line)
    for _ in range(num):
        line = ifile.readline()
        lst.append(tuple([ _ for _ in line.strip().split() ]))

    handle_list(lst, num)
