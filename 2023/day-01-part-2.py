import re
from helper import load_input_lines

def map_digit(c: str) -> int :
    if c.isdigit():
        return int(c)
    else:
        return {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
        }[c]

pattern = re.compile(r"three|seven|eight|zero|four|five|nine|six|one|two|\d", re.IGNORECASE | re.ASCII)

def extract_digits(s: str):
    start_idx = 0
    match = pattern.search(s, start_idx)
    while match:
        (start, end) = match.span()
        yield s[start:end]
        start_idx = start + 1
        match = pattern.search(s, start_idx)
        

def solve():
    sum = 0
    for line in load_input_lines(1):
        digits = [map_digit(c) for c in extract_digits(line)]
        first = digits[0]
        last  = digits[-1]
        factor = first * 10 + last
        sum += factor
    print(sum)


            

if __name__ == '__main__':
    solve()
