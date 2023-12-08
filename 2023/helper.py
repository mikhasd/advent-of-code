from typing import Generator
from pathlib import Path

aoc_2023 = Path(__file__).parent

def load_input(day: int) -> str:
    day_input_path = aoc_2023.joinpath(f'day-{day}.input.txt')
    if not day_input_path.exists():
        raise Exception(f'missing input file day-{day}.input.txt on directory {aoc_2023}')
    with day_input_path.open('r') as input_file:
        return input_file.read()

def load_input_lines(day: int) -> Generator[int, None, None]:
    day_input_path = aoc_2023.joinpath(f'day-{day}.input.txt')
    if not day_input_path.exists():
        raise Exception(f'missing input file day-{day}.input.txt on directory {aoc_2023}')
    with day_input_path.open('r') as input_file:
        line = input_file.readline()
        while line:
            yield line
            line = input_file.readline()


__all__ = [
    'load_input',
    'load_input_lines'
]