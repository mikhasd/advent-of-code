import re
from typing import Optional, Generator, Tuple, Set, Dict, List
from helper import load_input

NUMBERS = re.compile(r'\d+')

class Part:
    def __init__(self, n: int, length: int, x: int, y: int):
        self.n = n
        self.length = length
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'Part[n={self.n}; length={self.length}; x={self.x}; y={self.y}]'
    
    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Gear:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return other.x == self.x and other.y == self.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class EngineSchematic:

    def __init__(self, data: str) -> None:
        self.data = data
        # width of the matrix
        self.width = data.index('\n')

    def char_at(self, x: int, y: int) -> Optional[str]:
        # In case the provided index/position is negative, return None
        # the search algorithm will check negative positions for simplicity,
        if y < 0 or  x < 0 or x >= self.width - 1:
            return None
        
        line_start = y * (self.width + 1)
        pos = line_start + x
        
        if pos >= len(self.data):
            return None
        
        char = self.data[pos]
        if char == '\n' or char == '.':
            return None
        else:
            return char
        
    def has_gear_at(self, x: int, y: int) -> bool:
        c = self.char_at(x, y)
        if c == '*':
            return True
        return False
    
    def _find_pos(self, idx: int) -> Tuple[int, int]:
        y, x = divmod(idx, self.width + 1)
        return x, y

    
    def parts(self) -> Generator[Part, None, None]:
        for m in NUMBERS.finditer(self.data):
            value = m.string[m.start():m.end()]
            x, y = self._find_pos(m.start())            
            yield Part(int(value), len(value), x, y)

    def find_adjacent_gears(self, p: Part) -> Set[Gear]:
        gears: Set[Gear] = set()

        if self.has_gear_at(p.x - 1, p.y):
            gears.add(Gear(p.x - 1, p.y))

        if self.has_gear_at(p.x + p.length, p.y):
            gears.add(Gear(p.x + p.length, p.y))
        
        for x in range(p.x - 1, p.x + p.length + 1):
            for y in [p.y - 1, p.y + 1]:
                if self.has_gear_at(x, y):
                    gears.add(Gear(x, y))
        
        return gears



def solve():
    result = 0
    schematic = EngineSchematic(load_input(3))
    gear_to_parts: Dict[Gear, List[Part]] = dict()
    
    for p in schematic.parts():
        gears = schematic.find_adjacent_gears(p)
        if gears:
            for gear in gears:
                gear_parts = gear_to_parts.get(gear)
                if gear_parts:
                    gear_parts.append(p)
                else:
                    gear_to_parts[gear] = [p]

    result = 0

    for parts in gear_to_parts.values():
        if len(parts) == 2:
            gear_ratio = parts[0].n * parts[1].n
            result += gear_ratio

        
    print(result)
    

    

if __name__ == '__main__':
    solve()
