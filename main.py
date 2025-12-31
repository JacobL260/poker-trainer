import random

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

POSITION_RANGES = {
    "BB": ["22+", "A2s+", "A5o+", "K9s+", "KTo+", "Q9s+", "QTo+", "J9s+", "JTo", "T8s+", "98s", "87s", "76s", "65s", "54s"],
    "SB": ["22+", "A2s+", "A2o+", "K7s+", "K9o+", "Q8s+", "QTo+", "J8s+", "JTo", "T7s+", "97s+", "87s", "76s", "65s", "54s"],
    "BTN": ["22+", "A2s+", "A2o+", "K5s+", "K7o+", "Q7s+", "Q9o+", "J7s+", "J9o+", "T6s+", "96s+", "86s+", "76s", "65s", "54s"],
    "CO": ["22+", "A2s+", "A2o+", "K6s+", "K8o+", "Q8s+", "QTo+", "J8s+", "JTo", "T7s+", "97s+", "87s", "76s", "65s", "54s"],
    "HJ": ["22+", "A2s+", "A2o+", "K8s+", "KTo+", "Q9s+", "QTo+", "J9s+", "JTo", "T8s+", "98s", "87s", "76s", "65s", "54s"],
    "LJ": ["22+", "A2s+", "A2o+", "K9s+", "KTo+", "Q9s+", "QTo+", "J9s+", "JTo", "T8s+", "98s", "87s", "76s", "65s", "54s"],
    "EP": ["22+", "A2s+", "A2o+", "K9s+", "KTo+", "Q9s+", "QTo+", "J9s+", "JTo", "T8s+", "98s", "87s", "76s", "65s", "54s"],
    "UTG+1": ["22+", "A2s+", "A2o+", "K9s+", "KTo+", "Q9s+", "QTo+", "J9s+", "JTo", "T8s+", "98s", "87s", "76s", "65s", "54s"],
    "UTG": ["22+", "A2s+", "A2o+", "K9s+", "KTo+", "Q9s+", "QTo+", "J9s+", "JTo", "T8s+", "98s", "87s", "76s", "65s", "54s"],
} # Needs to be actually verified and then needs the notation of "+" to be expaned to actual hands

POSITIONS = list(POSITION_RANGES.keys())

def highlighted_range_chart(range_list):
    """ Takes a list of poker hands and prints a color-coded grid.
        Hands in range_list are shown in green, others in red."""
    card_grid = []

    for i in range(len(CARDS)):
        row = []
        for j in range(len(CARDS)):
            if i == j:
                pair = CARDS[i] + CARDS[j]
            elif i < j:
                pair = CARDS[i] + CARDS[j] + "s"
            else:
                pair = CARDS[j] + CARDS[i] + "o"

            # Green if in range_list, red otherwise
            if pair in range_list:
                row.append(f"\033[32m{pair}\033[0m")  # Green text
            else:
                row.append(f"\033[31m{pair}\033[0m")  # Red text
        card_grid.append(row)

    for row in card_grid:
        print(" ".join(row))
    print("\nLegend: \033[32mGreen\033[0m = In Range, \033[31mRed\033[0m = Out of Range")

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

# ----- Quiz Functions -----
def question_people_in_front():
    """Ask: 'How many people are in front of you?'"""
    position = random.choice(POSITIONS)
    print(f"Everyone has folded to you in the {position}.")
    answer = int(input("How many people are in front of you? "))
    correct = POSITIONS.index(position)
    if answer == correct:
        print("Correct! ✅")
    else:
        print(f"Wrong. The correct answer is {correct}.")

def question_position_from_people():
    """Ask: 'If there are X people in front of you, what position are you?'"""
    num_people = random.randint(0, len(POSITIONS)-1)
    print(f"There are {num_people} people in front of you.")
    print(f"The possible positions are: {', '.join(POSITIONS)}")
    answer = input("Which position are you? ").strip()
    correct = POSITIONS[num_people]
    if answer.upper() == correct:
        print("Correct! ✅")
    else:
        print(f"Wrong. The correct answer is {correct}.")

def expand_position_ranges(position_ranges):
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

def main():
    expanded = expand_position_ranges(POSITION_RANGES)

    highlighted_range_chart(expanded["UTG"])

    counter = 0
    questions = [question_people_in_front, question_position_from_people]
    while True:
        random.choice(questions)()  # Pick a random question
        counter = counter + 1
        print(f"You have answered {counter} questions.\n")
                
if __name__ == "__main__":
    main()