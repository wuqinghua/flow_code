#!/usr/bin/python

flow_list = list()
for line in open('flow_pairs.txt'):
    t = line.strip().split()[0]
    flow_list.append(t)

group = 20000

ofile = open('clean_flows.txt', 'w')
start = 0
while start < len(flow_list):
    end = start + group
    flows = flow_list[start:end]

    dic = dict()
    for flow in flows:
        dic[flow] = list()

    for line in open('dl.flow.txt'):
        t = tuple([ _ for _ in line.strip().split() ])
        if dic.has_key(t[0]):
            dic[t[0]].append(t)

    for k, v in dic.iteritems():
        if len(v) > 0:
            v.sort(key=lambda x:x[7])
            ofile.write('%d\n' % (len(v)))
            for t in v:
                ofile.write('%s\n' % (' '.join(list(t))))

    del dic
    start = end

ofile.close()
