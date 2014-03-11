#!/usr/bin/python

ofile = open('flow_index.txt', 'w')
ifile = open('../flow_data/clean_flows.txt')

count = 0
while True:
    line = ifile.readline()
    if line == '':
        break

    count += 1
    num = int(line)
    # buffers = ifile.readlines(num)
    for _ in range(num):
        if _ == num-1:
            line = ifile.readline()
        else:
            ifile.readline()

    flow = line.strip().split()[0]

    # including begin and end 
    ofile.write('%s %d %d\n' % (flow, count+1, count+num))
    count += num

ifile.close()
ofile.close()
