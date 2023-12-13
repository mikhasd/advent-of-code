from typing import Tuple, List, Iterable
from helper import load_input_lines
from itertools import product, chain

def parse_row(line: str) -> Tuple[str, List[int]]:
    space = line.index(' ')
    row = line[0:space]
    defects = list(map(int,line[space+1:].split(',')))
    return row, defects


def generate_options(row: str, defects: List[int]) -> Iterable[int]:
    known_defects = sum(defects)
    slots = len(defects)
    max_length = len(row)
    max_column_length = max_length - known_defects - (slots - 2)

    columns = [range(0, max_column_length + 1)] # first column can start at 0
    
    columns = columns + ([range(1, max_column_length + 1)] * (slots - 1))
    
    for option in product(*columns):
        option = list(option)
        if sum(option) + known_defects <= max_length:
            yield list(chain.from_iterable(zip(option, defects)))


def option_match_row(row: str, option: Iterable[int]) -> bool:
    row_idx = 0
    for opt_idx, length in enumerate(option):
        if opt_idx % 2 == 0:
            c = '.'
        elif c != '.':
            # check if theres a . before #
            return False
        else:
            c = '#'

        for _ in range(0, length):
            if row[row_idx] != '?' and row[row_idx] != c:
                return False
            row_idx += 1

    for c in row[row_idx:]:
        # checks the rest of the row
        if c == '#':
            return False
    
    return True

def count_options(row: List[str], defects: List[int]) -> int:
    count = 0
    for option in generate_options(row, defects):
        if option_match_row(row, option):
            count+= 1

    return count


def solve():
    total = 0
    for line in load_input_lines(12):
        row, defects = parse_row(line)
        options = count_options(row, defects)
        total += options
    print(total)
    

if __name__ == '__main__':
    solve()