#!/usr/bin/python

import fileinput

lst = list()
for line in fileinput.input():
    _ = line.strip().split()
    # time, dir, seq, ack, flag, len
    t = (float(_[7]), _[2], int(_[4]), int(_[5]), _[3], _[6])
    lst.append(t)

lst.sort(key=lambda x:x[0])

time = lst[0][0]
dir = lst[0][1]
seq = lst[0][2]
ack = lst[0][3]

num = dict()
if dir == 'IN':
    num['IN']  = [ seq, ack ]
    num['OUT'] = [ ack, seq ]
else:
    num['IN']  = [ ack, seq ]
    num['OUT'] = [ seq, ack ]

for t in lst:
    d = num[t[1]]
    print '%3.6f\t%3s\t%8d\t%8d\t%2s\t%8s' % (t[0]-time, t[1], t[2]-d[0], t[3]-d[1], t[4], t[5])
