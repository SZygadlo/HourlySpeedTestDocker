#!/bin/python3

from pingpy import ping

p = ping(timeout=5)
print(p.avgPing, p.maxPing, p.minPing, p.packetLoss)