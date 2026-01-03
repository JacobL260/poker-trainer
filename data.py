from utils import out_of_range_edge_cases, expand_position_ranges

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
}

RFI_RANGES = expand_position_ranges(RFI_RANGES_SHORTHAND)

POSITIONS = list(RFI_RANGES_SHORTHAND.keys())

RFI_RANGES_OUTSIDE = out_of_range_edge_cases(RFI_RANGES)