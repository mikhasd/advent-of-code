import re
from typing import Set, Iterator
from helper import load_input_lines
import math

CARD = re.compile(r'^Card\s+(?P<id>\d+):(?P<winning>[\d\s]+)\|(?P<game>[\d\s]+)$')
NUMBER = re.compile(r'\d+')

class Card:

    def __init__(self, id: int, winning: Set[int], game: Set[int]):
        self.id = id
        self.winning = winning
        self.game = game

    def matches(self) -> set[int]: 
        return self.winning.intersection(self.game)
    
    def points(self) -> int:
        matches = len(self.matches())
        if matches:
            return int(math.pow(2, matches - 1))
        else:
            return 0


def str_to_ints(s: str) -> Iterator[int]:
    return map(int, filter(lambda x: len(x), s.split(' ')))


def parse_card(line: str) -> Card:
    m = CARD.match(line)
    if not m:
        raise Exception(f'line did not match {line}')
    
    card_id = int(m.group('id'))
    winning = set(str_to_ints(m.group('winning')))
    game = set(str_to_ints(m.group('game')))
    return Card(card_id, winning, game)

def solve():
    points = 0
    for card in map(parse_card, load_input_lines(4)):
        points += card.points()
    print(int(points))
        
    

if __name__ == '__main__':
    solve()
