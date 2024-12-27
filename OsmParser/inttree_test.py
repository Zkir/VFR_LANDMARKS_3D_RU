from intervaltree import Interval, IntervalTree

t = IntervalTree()


t[1:1.9] = "interval 1"
t[1:1.9] = "interval 1a"
t[2.1:5.56] = "interval 1"
print(t)

print(t[1.5])