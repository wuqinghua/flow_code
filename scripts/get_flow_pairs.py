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
		t1, t2 = line.strip().split()[:2]
		
	if (t1, t2) in container:
		pass
	else:
    	container.add((t1, t2))
    	ofile.write('%s %s\n' % (t1, t2))

ofile.close()
