#!/usr/bin/python

container = set()

ofile = open('flow_pairs.txt', 'w')
for line in open('flow_pairs.txt.tmp'):
    t1, t2 = line.strip().split()
    if (t1, t2) in container:
        continue

    container.add((t1, t2))
    ofile.write('%s %s\n' % (t1, t2))
ofile.close()
