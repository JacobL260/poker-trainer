import random

from questions import *

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

RFI_RANGES_SHORTHAND = {
    "BB": ["AA"],
    "SB": ["22+", "A2s+", "K2s+", "Q2s+", "J2s+", "T2s+", "92s+", "82s+", "72s+", "62s+", "52s+", "42s+", "32s", "A2o+", "K2o+", "Q2o+", "J2o+", "T3o+", "95o+", "85o+", "75o+", "64o+", "54o"],
    "BTN": ["22+", "A2s+", "K2s+", "Q2s+", "J3s+", "T3s+", "95s+", "85s+,74s+,64s+,53s+,43s,A2o+,K5o+,Q8o+,J8o+,T7o+,97o+,87o"],
    "CO": ["22+", "A2s+", "K2s+","Q5s+","J7s+","T6s+","96s+","86s+","75s+","65s","54s","A5o+","K9o+","Q9o+","J9o+","T9o"],
    "HJ": ["22+", "A2s+", "K4s+", "Q8s+", "J8s+", "T7s+", "97s+", "87s", "76s", "65s", "54s", "A8o+", "KTo+", "QTo+", "JTo"],
    "LJ": ["33+", "A2s+", "K6s+", "Q9s+", "J8s+", "T8s+", "98s", "87s", "76s", "A9o+", "KTo+", "QTo+"],
    "UTG+2": ["44+", "A2s+", "K8s+", "Q9s+", "J9s+", "T8s+", "98s", "76s", "ATo+", "KTo+"],
    "UTG+1": ["66+", "A3s+", "K8s+", "Q9s+", "J9s+", "T9s", "98s", "ATo+"],
    "UTG": ["66+", "A3s+", "K9s+", "Q9s+", "AJo+", "KQo"],
} # 

def expand_position_ranges(position_ranges):
    """ Takes a dictionary of position ranges and expands shorthand notation
    and returns a new dictionary with full hand lists."""
    expanded_ranges = {}
    for position in position_ranges:
        hands = position_ranges[position]
        expanded = []

        for hand in hands:
            if len(hand) == 3 and hand[0] == hand[1] and hand[2] == "+":
                start_index = CARDS.index(hand[0])

                for i in range(start_index + 1):
                    card = CARDS[i]
                    expanded.append(card + card)

            elif len(hand) == 4 and hand[2] == "s" and hand[3] == "+":
                high_card = hand[0]
                start_index = CARDS.index(hand[1])

                for i in range(start_index + 1):
                    low_card = CARDS[i]
                    if low_card != high_card:
                        expanded.append(high_card + low_card + "s")

            elif len(hand) == 4 and hand[2] == "o" and hand[3] == "+":
                high_card = hand[0]
                start_index = CARDS.index(hand[1])

                for i in range(start_index + 1):
                    low_card = CARDS[i]
                    if low_card != high_card:
                        expanded.append(high_card + low_card + "o")

            else:
                expanded.append(hand)

        # remove duplicates, keep order
        unique_expanded = []
        for h in expanded:
            if h not in unique_expanded:
                unique_expanded.append(h)

        expanded_ranges[position] = unique_expanded

    return expanded_ranges

RFI_RANGES = expand_position_ranges(RFI_RANGES_SHORTHAND)

def out_of_range_edge_cases(position_ranges):
    """Given a dictionary of ranges in shorthand notation, returns a dictionary
    of edge case hands that are just outside the defined ranges for each position.
    
    Works for worst PAIRS, CONNECTORS, and ONE-CARD-LOWER
    """
    edge_cases = {}
    for position in position_ranges:
        hands = position_ranges[position]
        edges = []
    
        for hand in hands:
            index0 = CARDS.index(hand[0])
            index1 = CARDS.index(hand[1])
            if hand[0] == hand[1]: # Pair
                if index0 + 1 < len(CARDS):
                    lower_pair = CARDS[index0 + 1] + CARDS[index1 + 1]
                    if lower_pair not in hands:
                        edges.append(lower_pair)
            elif abs(index0 - index1) == 1: # Connectors
                if index0 + 1 < len(CARDS) and index1 + 1 < len(CARDS):
                    lower_connector = CARDS[index0 + 1] + CARDS[index1 + 1] + hand[2]
                    if lower_connector not in hands:
                        edges.append(lower_connector)
            elif hand[-1] == "+": # Playable hand range "A9s+"
                if index0 + 1 < len(CARDS) and index1 + 1 < len(CARDS):
                    lower_hand = hand[0] + CARDS[index1+1] + hand[2] # Do not inlucde "+""
                    if lower_hand not in hands:
                        edges.append(lower_hand)            
                

        unique_edges = []
        for h in edges:
            if h not in unique_edges:
                unique_edges.append(h)

        edge_cases[position] = unique_edges

    return edge_cases

test = out_of_range_edge_cases(RFI_RANGES_SHORTHAND)

POSITIONS = list(RFI_RANGES_SHORTHAND.keys())

def range_chart(cards, colored_ranges=None, default_color=None):
    """
    Prints a poker range chart.

    cards: list of card ranks (e.g. ["A","K","Q",...,"2"])
    colored_ranges: list of tuples -> [(set_of_hands, "color_name"), ...]
    (red, green, yellow, blue, magenta, cyan, reset)
    default_color: color for hands not in any range (None = no color)
    """

    ANSI_COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
    }

    colored_ranges = colored_ranges or []

    for i in range(len(cards)):
        row = []
        for j in range(len(cards)):
            # Build hand label
            if i == j:
                hand = cards[i] + cards[j]
            elif i < j:
                hand = cards[i] + cards[j] + "s"
            else:
                hand = cards[j] + cards[i] + "o"

            # Determine color
            color = default_color
            for hand_set, hand_color in colored_ranges:
                if hand in hand_set:
                    color = hand_color
                    break

            # Apply color only if requested
            if color:
                hand = f"{ANSI_COLORS[color]}{hand}{ANSI_COLORS['reset']}"

            row.append(hand)

        print(" ".join(row))

def random_hand():
    """Generates a random poker hand in standard notation."""
    card1 = random.choice(CARDS)
    card2 = random.choice(CARDS)
    if card1 == card2:
        return card1 + card2
    else:
        suited = random.choice([True, False])
        if suited:
            if CARDS.index(card1) < CARDS.index(card2):
                return card1 + card2 + "s"
            else:
                return card2 + card1 + "s"
        else:
            if CARDS.index(card1) < CARDS.index(card2):
                return card1 + card2 + "o"
            else:
                return card2 + card1 + "o"

def main():
    """range_chart(CARDS, colored_ranges=[(RFI_RANGES["SB"], "green")])
    counter = 0
    questions = [question_people_in_front, question_position_from_people]
    while True:
        random.choice(questions)()  # Pick a random question
        counter = counter + 1
        print(f"You have answered {counter} questions.\n")"""
    range_chart(CARDS, [(RFI_RANGES["UTG"],"green"), (test["UTG"],"red")])

if __name__ == "__main__":
    main()