import re
from typing import Set, Iterator, Dict, List, Tuple, Optional
from helper import load_input_lines

MAP_START = re.compile(r'^(?P<source>\w+)-to-(?P<destination>\w+) map:$')
MAPPING_LINE = re.compile(r'^(?P<dest_start>\d+) (?P<src_start>\d+) (?P<length>\d+)$')

class Mapping:
    dest_start: int
    dest_type: str
    src_start: int
    length: int

    def __init__(self, src_start: int, dest_type: str, dest_start: int, length: int) -> None:
        self.dest_start = dest_start
        self.src_start = src_start
        self.length = length
        self.dest_type = dest_type        

    def find_location(self, src: int) -> Optional[int]:
        if self.src_start <= src < self.src_start + self.length:
            d = src - self.src_start
            return self.dest_start + d
        return None

class Almanac:    
    maps: Dict[str, List[Mapping]] = dict()
    
    def add_mappings(self, src_type: str, mappings: List[Mapping]):
        self.maps[src_type] = mappings

    def find_location(self, src: int, src_type: str = 'seed') -> Tuple[int, str]:
        mappings = self.maps.get(src_type, None)
        if not mappings:
            return src, src_type
        
        for mapping in mappings:
            loc = mapping.find_location(src)
            if loc:
                return self.find_location(loc, mapping.dest_type)
        
        return src, src_type
    




def parse_seeds_line(seeds_line: str) -> Set[int]:
    # seeds: (\d+) \n
    return set(map(int, seeds_line[7:-1].split(' ')))


def parse_map(almanac: Almanac, lines: Iterator[str], source_type: str, destination_type: str):
    mappings: List[Mapping] = list()
    for line in lines:
        if not line or line == '\n':
            break
        
        m = MAPPING_LINE.match(line)
        dest_start = int(m.group('dest_start'))
        src_start = int(m.group('src_start'))
        length = int(m.group('length'))

        mapping = Mapping(src_start, destination_type, dest_start, length)
        mappings.append(mapping)

    mappings.sort(key=lambda m: m.src_start)
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
            parse_map(almanac, lines, source_type, destination_type)

    locations = [almanac.find_location(seed)[0] for seed in seeds]
    print(min(locations))
    
    

    

if __name__ == '__main__':
    solve()