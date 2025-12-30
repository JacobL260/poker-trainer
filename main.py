import pandas as pd

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
rank = {card: i for i, card in enumerate(CARDS)}

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
        row.append(pair)
    card_grid.append(row)

df = pd.DataFrame(card_grid)

PF_RANGE = ["AA", "K7s"]

for i in range(len(PF_RANGE)):
    if PF_RANGE[i] in df.values:
        result = df.isin([PF_RANGE[i]])
        position = result.stack()[result.stack()].index[0]
        print(f"Found {PF_RANGE[i]} at position: {position}")

print(df)