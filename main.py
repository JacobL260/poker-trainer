import random

from questions import *
from utils import *
from data import *

RFI_RANGES = expand_position_ranges(RFI_RANGES_SHORTHAND)

def main():
    """test = out_of_range_edge_cases(RFI_RANGES)
    range_chart(CARDS, [(RFI_RANGES["UTG"],"green"), (test["UTG"],"red")])
    range_chart(CARDS, colored_ranges=[(RFI_RANGES["SB"], "green")])"""
    counter = 0
    questions = [question_out_of_range]
    while True:
        random.choice(questions)()  # Pick a random question
        counter = counter + 1
        print(f"You have answered {counter} questions.\n")

if __name__ == "__main__":
    main()