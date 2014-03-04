#!/usr/bin/python

min, max = 0, 0

for line in open('dl.flow.txt'):
    time = float(line.strip().split()[7])
    if min == 0 or min > time:
        min = time

    if max == 0 or max < time:
        max = time


print min, max
