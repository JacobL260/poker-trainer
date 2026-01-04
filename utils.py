import random
from constants import CARDS

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
        
def out_of_range_edge_cases(position_ranges):
    """Given a dictionary of playable hands, returns a dictionary
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

            if len(hand) > 2:
                suit = hand[2]
            else:
                suit = ""

            if index0 + 1 < len(CARDS) and index1 + 1 < len(CARDS): # Verify that there is a lower card
                if hand[0] == hand[1]: # Pair
                    lower_pair = CARDS[index0 + 1] + CARDS[index1 + 1]
                    if lower_pair not in hands:
                        edges.append(lower_pair)
                else:
                    if abs(index0 - index1) == 1:
                        lower_connector = CARDS[index0 + 1] + CARDS[index1 + 1] + hand[2]
                        if lower_connector not in hands:
                            edges.append(lower_connector)
                            
                    lower_hand = hand[0] + CARDS[index1 + 1] + suit
                    lower_rank = CARDS[index1 + 1]

                    if hand[0] == lower_rank:
                        lower_hand = hand[0] + lower_rank
                    else:
                        lower_hand = hand[0] + lower_rank + suit

                    if lower_hand not in hands:
                        edges.append(lower_hand)

        unique_edges = []
        for h in edges:
            if h not in unique_edges:
                unique_edges.append(h)

        edge_cases[position] = unique_edges

    return edge_cases