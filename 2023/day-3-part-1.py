import re
from typing import Optional, Generator, Tuple
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
        
    def has_symbol_at(self, x: int, y: int) -> bool:
        c = self.char_at(x, y)
        if c and not c.isdigit():
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

    def has_adjacent_symbol(self, p: Part) -> bool:
        if self.has_symbol_at(p.x - 1, p.y) or self.has_symbol_at(p.x + p.length, p.y):            
            return True
        
        for x in range(p.x - 1, p.x + p.length + 1):
            for y in [p.y - 1, p.y + 1]:
                if self.has_symbol_at(x, y):
                    return True
        return False



def solve():
    result = 0
    schematic = EngineSchematic(load_input(3))
    for p in schematic.parts():
        if schematic.has_adjacent_symbol(p):
          result += p.n
    print(result)
    

    

if __name__ == '__main__':
    solve()
