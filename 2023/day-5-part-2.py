import re
from itertools import chain
from typing import Iterator, Dict, List, Tuple, Optional, Self
from helper import load_input_lines

MAP_START = re.compile(r'^(?P<source>\w+)-to-(?P<destination>\w+) map:$')
MAPPING_LINE = re.compile(r'^(?P<dest_start>\d+) (?P<src_start>\d+) (?P<length>\d+)$')

class Range:
    start: int
    end: int

    def __init__(self, start: int, end: Optional[int]=None, elements: Optional[int]=None) -> None:
        self.start = start
        if elements:
            self.end = start + elements - 1
        elif end:
            self.end = end
        else:
            raise Exception('either "end" or "length" arguments must be provided')

    def __repr__(self) -> str:
        return f'Range[{self.start}:{self.end}]'
    
    def __str__(self: Self) -> str:
        return ' '.join(chain(
            map(lambda _: '  ', range(0, self.start)),
            map(lambda n: str(n) if n >= 10 else f' {n}', range(self.start, self.end + 1)),
            map(lambda _: '  ', range(self.end + 1, 100))
        ))

    def intersection(self, other: Self) -> Optional[Self]:
        if self.start <= other.start <= self.end or self.start <= other.end <= self.end:
            i_start = max(self.start, other.start)
            i_end = min(self.end, other.end)
            return Range(i_start, end=i_end)
        else:
            return None
        
    @property
    def elements(self) -> int:
        return self.end - self.start + 1


class Mapping:
    dest: Range
    src: Range
    dest_type: str

    def __init__(self, src: Range, dest: Range, dest_type: str) -> None:
        self.src = src
        self.dest = dest
        self.dest_type = dest_type

    def find_location(self, src: Range) -> Optional[Range]:
        if intersection := self.src.intersection(src):

            
            delta_start = intersection.start - self.src.start
            i_elements = intersection.elements

            destination = Range(self.dest.start + delta_start, elements=i_elements)

            return destination
        
        return None

class Almanac:    
    maps: Dict[str, List[Mapping]] = dict()
    path: Dict[str, str] = dict()
    
    def add_mappings(self, src_type: str, mappings: List[Mapping]):
        self.maps[src_type] = mappings

    def add_path(self, src: str, dest: str):
        self.path[src] = dest

    def find_location(self, src: Range, src_type: str = 'seed') -> Tuple[Range, str]:
        mappings = self.maps.get(src_type, None)
        if not mappings:
            return src, src_type

        for mapping in mappings:
            loc = mapping.find_location(src)
            if loc:
                return self.find_location(loc, mapping.dest_type)

        return self.find_location(src, self.path[src_type])
    




def parse_seeds_line(seeds_line: str) -> List[int]:
    # seeds: (\d+) \n
    return list(map(int, seeds_line[7:-1].split(' ')))


def parse_map(almanac: Almanac, lines: Iterator[str], source_type: str, destination_type: str):
    mappings: List[Mapping] = list()
    for line in lines:
        if not line or line == '\n':
            break
        
        m = MAPPING_LINE.match(line)
        dest_start = int(m.group('dest_start'))
        src_start = int(m.group('src_start'))
        length = int(m.group('length'))        
        mapping = Mapping(Range(src_start, elements=length), Range(dest_start, elements=length), destination_type)
        mappings.append(mapping)

    almanac.add_mappings(source_type, mappings)


def solve():
    lines = load_input_lines(5)
    seeds = parse_seeds_line(next(lines))
    almanac = Almanac()

    next(lines) # empty line

    for line in lines:
        m = MAP_START.match(line)        
        if m:
            source_type = m.group('source')
            destination_type = m.group('destination')
            almanac.add_path(source_type, destination_type)
            parse_map(almanac, lines, source_type, destination_type)

    shortest = 2**64

    for i in range(0, len(seeds), 2):
        start = seeds[i]
        count = seeds[i+1]
        seed_range = Range(start, elements=count)
        
        loc = almanac.find_location(seed_range)
        shortest = min(shortest, loc[0].start)
        print(f'done with seed {seed_range} = {loc[0]}')
    
    print(shortest)
    
    

    

if __name__ == '__main__':
    solve()