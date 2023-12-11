import re
#from typing import Generator
from functools import reduce
from helper import load_input_lines

NUMBERS = re.compile(r'\d+')


def solve():
    [time, distance] = [int(''.join([m.group() for m in NUMBERS.finditer(line)])) for line in load_input_lines(6) ]
    ways = len([h for h in range(1, time) if (h * time - h**2) > distance])

    print(ways)
        

    

if __name__ == '__main__':
    solve()

# d = h * (t - h)
# d = distance
# h = holding time
# t = total time