#import re
from typing import List
from helper import load_input_lines

def extract_values(line: str) -> List[int]:
    return [int(v) for v in line.split(' ')] 


def calculate_diferences(values: List[int]) -> List[int]:
    result = [None] * (len(values) - 1)
    for i in range(1, len(values)):
        result[i - 1] = values[i] - values[i - 1]
    return result



def calculate_prediction(values: List[int]) -> int:
    if all(map(lambda v: v == 0, values)):
        return 0

    diferences = calculate_diferences(values)
    prediction = values[0] - calculate_prediction(diferences)
    return prediction


def solve():
    solution = 0
    for line in load_input_lines(9):
        values = extract_values(line)
        prediction = calculate_prediction(values)
        solution += prediction
    print(solution)
    
    

if __name__ == '__main__':
    solve()