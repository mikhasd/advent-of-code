import re
from helper import load_input_lines

CUBE_COUNT = re.compile(r'(\d+) (green|red|blue)')

def parse_game(s: str) -> int:
    sets_start = s.index(':')
    sets_portions = s[sets_start:]
    r = 1
    g = 1
    b = 1

    for set_portion in sets_portions.split(';'):
        for cube_count_match in CUBE_COUNT.finditer(set_portion):
            count = int(cube_count_match.group(1))
            colour = cube_count_match.group(2)
            match colour:
                case 'red':
                    r = max(r, count)
                case 'green':
                    g = max(g, count)
                case 'blue':
                    b = max(b, count)
            
    power = r * g * b
    return power


def solve():
    s = sum([parse_game(line) for line in load_input_lines(2)])
            
    print(s)
    

if __name__ == '__main__':
    solve()
