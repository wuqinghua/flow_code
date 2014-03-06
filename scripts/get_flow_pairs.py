#!/usr/bin/python

import sys
container = set()

ofile = open('flow_pairs.txt', 'w')
ifile = open('/home/zhoujianer/360_flow/clean_flows.txt')

while True:
	line = ifile.readline()
	if line == '':
		break

	lst = list()
	num = int(line)
	for _ in range(num):
		line = ifile.readline()
    	lst.append(tuple([_ for _ in line.strip().split()]))
		
	t1 = lst[0][1]
	t2 = lst[0][0]
	#if (t1, t2) in container:
    print t1    

    #container.add((t1, t2))
    ofile.write('%s %s\n' % (t1, t2))
ofile.close()
