import re
from typing import Tuple
from helper import load_input_lines

GAME_ID_RE = re.compile(r'^Game (\d+):')
CUBE_COUNT = re.compile(r'(\d+) (green|red|blue)')

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

def parse_game(s: str) -> Tuple[int, bool]:
    m = GAME_ID_RE.search(s)
    game_id = int(m.group(1))

    sets_start = m.span()[1]
    sets_portions = s[sets_start:]
    for set_portion in sets_portions.split(';'):
        
        for cube_count_match in CUBE_COUNT.finditer(set_portion):
            count = int(cube_count_match.group(1))
            colour = cube_count_match.group(2)
            match colour:
                case 'red':
                    colour_max = MAX_RED
                case 'green':
                    colour_max = MAX_GREEN
                case 'blue':
                    colour_max = MAX_BLUE
            
            if count > colour_max:
                return (game_id, False)
    
    return (game_id, True)


def solve():
    sum = 0
    for line in load_input_lines(2):
        game = parse_game(line)
        if game[1]:
            sum += game[0]
            
    print(sum)
    

if __name__ == '__main__':
    solve()
