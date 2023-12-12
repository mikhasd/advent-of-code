import re
from typing import Generator, Tuple, Dict, Iterable
from helper import load_input_lines
import math

INSTRUCTION = re.compile(r'^(?P<source>\w{3})\s+=\s+\((?P<left>\w{3}),\s+(?P<right>\w{3})')

def add_map_node(map: Dict[str, Tuple[str, str]], line: str):
    m = INSTRUCTION.match(line)
    groups = m.groups()
    source = groups[0]
    left = groups[1]
    right = groups[2]
    map[source] = (left, right)

def count_steps(map: Dict[str, Tuple[str, str]], start_point: str, instructions: str) -> int:
    encoded_instructions = [0 if instruction == 'L' else 1 for instruction in instructions]
    node = map[start_point]
    steps = 0
    while True:
        for instruction in encoded_instructions:
            steps += 1
            next_node = node[instruction]
            node = map[next_node]
            if next_node[2] == 'Z':
                return steps

def solve():
    lines = load_input_lines(8)
    instructions = next(lines)[:-1] # remove trailing line break
    next(lines) # skip blank line
    map: Dict[str, Tuple[str, str]] = dict()
    for line in lines:
        add_map_node(map, line)

    starting_points = list(filter(lambda p: p[2] == 'A', map.keys()))
    print(f'starting points: {starting_points}')


    steps = [count_steps(map, starting_point, instructions) for starting_point in starting_points]
    print(math.lcm(*steps))


    

if __name__ == '__main__':
    solve()