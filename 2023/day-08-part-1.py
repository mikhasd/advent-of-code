import re
from typing import Generator, Tuple, Dict
from helper import load_input_lines

INSTRUCTION = re.compile(r'^(?P<source>\w{3})\s+=\s+\((?P<left>\w{3}),\s+(?P<right>\w{3})')

def add_map_node(map: Dict[str, Tuple[str, str]], line: str):
    m = INSTRUCTION.match(line)
    groups = m.groups()
    source = groups[0]
    left = groups[1]
    right = groups[2]
    map[source] = (left, right)


def solve():
    lines = load_input_lines(8)
    instructions = next(lines)[:-1] # remove trailing line break
    next(lines) # skip blank line
    map: Dict[str, Tuple[str, str]] = dict()
    for line in lines:
        add_map_node(map, line)

    node = map['AAA']
    steps = 0
    while True:
        for instruction in instructions:
            steps += 1
            next_point = node[0] if instruction == 'L' else node[1]
            if next_point == 'ZZZ':
                print(steps)
                return
            
            node = map[next_point]


    

if __name__ == '__main__':
    solve()