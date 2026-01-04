import random

from constants import *
from data import *
from utils import *

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
    print(f"The possible positions are: {', '.join(random.sample(POSITIONS, len(POSITIONS)))}")
    answer = input("Which position are you? ").strip()
    correct = POSITIONS[num_people]
    if answer.upper() == correct:
        print("Correct! ✅")
    else:
        print(f"Wrong. The correct answer is {correct}.")

def question_out_of_range():
    """Ask: 'If this hand is given to you in the POSITION first to act, should you raise?'"""
    position = random.choice(POSITIONS[1:])
    print(f"You are the {position} and first to act.")

    hand = random.choice(RFI_RANGES_OUTSIDE[position])
    print(f"You are dealt: {hand}")

    answer = input("Should you raise? Y/N : ")
    if answer.upper() == "N":
        print("Correct! ✅")
    else:
        print("WRONG ❌")
        range_chart(
            CARDS,
            [(RFI_RANGES_OUTSIDE[position], "red"), (RFI_RANGES[position], "green")]
        )

def question_in_of_range():
    """Ask: 'If this hand is given to you in the POSITION first to act, should you raise?'"""
    position = random.choice(POSITIONS[1:])
    print(f"You are the {position} and first to act.")

    hand = random.choice(RFI_RANGES[position])
    print(f"You are dealt: {hand}")

    answer = input("Should you raise? Y/N : ")
    if answer.upper() == "Y":
        print("Correct! ✅")
    else:
        print("WRONG ❌")
        range_chart(
            CARDS,
            [(RFI_RANGES[position], "green")]
        )