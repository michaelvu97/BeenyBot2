from fuzzywuzzy import fuzz
from products_list import getProductsList

"""
Returns a product list id, and a confidence (0,100)
"""
def getProductName(search_str):
    # Also look at fuzz.partial_ratio
    ratios = [(x, fuzz.ratio(search_str, x)) for x in getProductsList()]

    best_ratio = 0
    best_idx = 0

    # TODO: get the best ratio and the best element so far
    for i in range(len(ratios)):
        ratio = ratios[i]
        if ratios[1] < best_ratio: 
            continue
        best_ratio = ratios[1]
        best_idx = i

    return best_idx, best_ratio


if __name__ == "__main__":
    # Tests
    test = [
        "ketchup",
        "pizza",
        "organic",
        "kombucha",
        "shrimp"
    ]

    print([getProductName(x) for x in test])