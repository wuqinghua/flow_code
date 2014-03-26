#!/usr/bin/python

flow_list = list()
for line in open('../flow_data/20140319_flows.txt'):
    t = line.strip()
    flow_list.append(t)

group = 100000

ofile = open('../flow_data/20140319_plain_sorted.txt', 'w')
start = 0
while start < len(flow_list):
    end = start + group
    flows = flow_list[start:end]

    dic = dict()
    for flow in flows:
        dic[flow] = list()

    i = 0
    for line in open('../flow_data/20140319_plain.txt'):
        t = tuple([ _ for _ in line.strip().split() ])
        if dic.has_key(t[0]):
            dic[t[0]].append(t)
        i += 1
        if i % 10000000 == 0:
            print start, i

    for k, v in dic.iteritems():
        if len(v) > 0:
            v.sort(key=lambda x:x[7])
            ofile.write('%d\n' % (len(v)))
            for t in v:
                ofile.write('%s\n' % (' '.join(list(t))))

    del dic
    start = end

ofile.close()
