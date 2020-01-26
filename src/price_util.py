
def priceToNum(s):
    isCents = False
    isDollars = False

    if ('¢' in s):
        isCents = True
    elif ('$' in s) or ('.' in s):
        isDollars = True
    
    if isCents:
        return float(clean(s)) / 100

    if len(s) > 2:
        return float(clean(s)) / 100

    return float(clean(s))

def clean(s):
    return s.strip(' ¢$').replace('.', '')


if __name__ == "__main__":
    # Tests
    tests = [
        "$4.50",
        "$4",
        "4",
        "499",
        "$499",
        "99¢",
        "99",
        "4.50"
    ]

    for test in tests:
        print(test + "->" + str(priceToNum(test)))