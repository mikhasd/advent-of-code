#import re
from typing import Dict, Tuple
from helper import load_input_lines
from functools import reduce

HandType = int

HAND_TYPE_HIGH_CARD: HandType = 1
HAND_TYPE_ONE_PAIR: HandType = 2
HAND_TYPE_TWO_PAIR: HandType = 3
HAND_TYPE_THREE_OF_KIND: HandType = 4
HAND_TYPE_FULL_HOUSE: HandType = 5
HAND_TYPE_FOUR_OF_KIND: HandType = 6
HAND_TYPE_FIVE_OF_KIND: HandType = 7

CARD_WEIGHTS: Dict[str, int] = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 1,
    'T': 10
}


def compare_cards(c1: str, c2: str) -> int:
    w1 = CARD_WEIGHTS.get(c1) or int(c1)
    w2 = CARD_WEIGHTS.get(c2) or int(c2)
    return w1 - w2


def determine_hand_type(cards: str) -> HandType:
    def grouping(m: Dict[str, int], card: str) -> Dict[str, int]:
        count = m.get(card, 0)
        count += 1
        m[card] = count
        return m
    
    grouped_cards = reduce(grouping, sorted(cards), {})
    pairs = 0
    has_three_of_kind = False
    jokers = 0
    hand_type = HAND_TYPE_HIGH_CARD
    for card, count in grouped_cards.items():
        if card == 'J':
            jokers = count
        elif count == 5:
            return HAND_TYPE_FIVE_OF_KIND
        elif count == 4:
            hand_type = HAND_TYPE_FOUR_OF_KIND
        elif count == 3:
            has_three_of_kind = True
        elif count == 2:
            pairs += 1

    if jokers == 5:
        return HAND_TYPE_FIVE_OF_KIND
    elif jokers == 4:
        return HAND_TYPE_FOUR_OF_KIND
    elif jokers == 3:
        if pairs:
            return HAND_TYPE_FIVE_OF_KIND
        else:
            return HAND_TYPE_FOUR_OF_KIND
    elif jokers == 2:
        if pairs or has_three_of_kind:
            return HAND_TYPE_FULL_HOUSE
        else:
            return HAND_TYPE_THREE_OF_KIND
    elif jokers == 1:
        if hand_type == HAND_TYPE_FOUR_OF_KIND:
            return HAND_TYPE_FIVE_OF_KIND
        elif has_three_of_kind:
            return HAND_TYPE_FOUR_OF_KIND
        elif pairs == 2:
            return HAND_TYPE_FULL_HOUSE
        elif pairs == 1:
            return HAND_TYPE_THREE_OF_KIND
        else:
            return HAND_TYPE_ONE_PAIR

    if hand_type == HAND_TYPE_FOUR_OF_KIND:
        return HAND_TYPE_FOUR_OF_KIND
    
    if has_three_of_kind:
        if pairs:
            return HAND_TYPE_FULL_HOUSE
        else:
            return HAND_TYPE_THREE_OF_KIND
        
    if pairs == 2:
        return HAND_TYPE_TWO_PAIR
    elif pairs == 1:
        return HAND_TYPE_ONE_PAIR

    return HAND_TYPE_HIGH_CARD
    


class HandAndScore:
    cards: str
    type: HandType
    score: int

    def __init__(self, cards: str, type: HandType, score: int) -> None:
        self.cards = cards
        self.type = type
        self.score = score

    def __repr__(self) -> str:
        type_str = ({
            HAND_TYPE_ONE_PAIR: 'Pair',
            HAND_TYPE_TWO_PAIR: '2x Pair',
            HAND_TYPE_THREE_OF_KIND: '3X',
            HAND_TYPE_FULL_HOUSE: 'Full House',
            HAND_TYPE_FOUR_OF_KIND: '4X',
            HAND_TYPE_FIVE_OF_KIND: '5X'
        }).get(self.type, 'High Card')
        joker = '*' if 'J' in self.cards else ''
            
        return f'Hand[cards: {self.cards}{joker}, type: {type_str}]'
    
    def __cmp__(self, other) -> int:
        if self.type != other.type:
            return self.type - other.type

        for i in range(0, 5):
            if r := compare_cards(self.cards[i], other.cards[i]):
                return r
            
        return 0
    
    def __lt__(self, other) -> bool:
        return self.__cmp__(other) < 0
    
    def __gt__(self, other) -> bool:
        return self.__cmp__(other) > 0
    
    def __le__(self, other) -> bool:
        return self.__cmp__(other) <= 0
    
    def __ge__(self, other) -> bool:
        return self.__cmp__(other) <= 0
    
    def __eq__(self, other) -> bool:
        return self.__cmp__(other) == 0
    

def to_scored_hand(s: str) -> HandAndScore:
    [cards, score] = s.split(' ')
    hand_type = determine_hand_type(cards)
    return HandAndScore(cards, hand_type, int(score))


def solve():
    sorted_hands = sorted(map(to_scored_hand, load_input_lines(7)))
    total_score = 0
    for i, hand in enumerate(sorted_hands):
        print(f'{(i+1)} -> {hand} -> {hand.score}')
        hand_score = (i+1) * hand.score
        total_score += hand_score

    print(total_score)
    
    

if __name__ == '__main__':
    solve()