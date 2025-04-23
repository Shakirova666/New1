#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

ax, ay = map(float, input('Введите ax и ay').split())
a = R2Point(ax, ay)
bx, by = map(float, input('Введите bx и by').split())
b = R2Point(bx, by)
f = Void(a, b)
try:
    while True:
        f = f.add(R2Point())
        print(
            f"S = {f.area()}, \nP = {f.perimeter()}, \nКол-во ребер вне 1-окр (a, b) = {f.count}")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
