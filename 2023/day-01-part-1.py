from helper import load_input_lines

def solve():
    sum = 0
    for line in load_input_lines(1):
        digits = [int(c) for c in line if c.isdigit()]
        first = digits[0]
        last = digits[-1]
        factor = first * 10 + last
        sum += factor
    print(sum)
            

if __name__ == '__main__':
    solve()
