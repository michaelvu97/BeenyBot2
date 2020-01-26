import re
import sys
from price_util import priceToNum

def parsePromo(big_text, whole_text):
    minNumber = 1
    discount = None
    dollarsPerUnit = None
    dollarsOffPerUnit = None

    try:
        if detectFree(big_text):
            discount = 0.5
            minNumber = 2
        elif detectHalf(big_text):
            discount = 0.5
        elif detectPercent(big_text):
            discount = float(int(big_text[:big_text.find('%')].strip())) / 100
        elif detectOff(big_text):
            dollarsOffPerUnit = priceToNum(big_text[:big_text.find("OFF")])
        elif re.search("([0-9]+)[^0-9.$]+([0-9\.\$]+)",big_text):
            matches = re.search("([0-9]+)[^0-9]+([0-9\.\$]+)",big_text)
            minNumber = int(matches.group(1))
            totalCost = priceToNum(matches.group(2))
            dollarsPerUnit = totalCost / minNumber
        else:
            matches = re.search("([0-9\.\$]+)", big_text)
            dollarsPerUnit = priceToNum(matches.group(1))
    except:
        sys.exc_info()
        return None

    try:
        # Detect the savings
        saveText = whole_text[whole_text.find('SAVE') + 4:]
        saveText = saveText[:saveText.find('\n')]
        if minNumber > 1 and " on " in saveText:
            priceStr = saveText[:saveText.find(" on " )]
            dollarsOffPerUnit = priceToNum(priceStr) / minNumber
        elif "/" in saveText:
            priceStr = saveText[:saveText.find("/")]
            dollarsOffPerUnit = priceToNum(priceStr)
        elif "l" in saveText:
            priceStr = saveText[:saveText.find("l")]
            dollarsOffPerUnit = priceToNum(priceStr)
        elif "I" in saveText:
            priceStr = saveText[:saveText.find("I")]
            dollarsOffPerUnit = priceToNum(priceStr)
        else:
            matches = re.search("([0-9\.$]+)", saveText)
            dollarsOffPerUnit = priceToNum(matches.group(1))
    except:
        sys.exc_info()

    # Infer the required fields
    try:
        if discount is None and dollarsPerUnit is not None and dollarsOffPerUnit is not None:
            discount = dollarsOffPerUnit / (dollarsOffPerUnit + dollarsPerUnit)
        if dollarsOffPerUnit is None and discount is not None and dollarsPerUnit is not None:
            dollarsOffPerUnit = discount * dollarsPerUnit / (1.0 - discount)
        if dollarsPerUnit is None and discount is not None and dollarsOffPerUnit is not None:
            dollarsPerUnit = (dollarsOffPerUnit / discount) - dollarsOffPerUnit
    except:
        sys.exc_info()

    # Correction
    if discount is not None:
        if discount > 1:
            discount = None
        elif discount < 0:
            discount = None

    if dollarsOffPerUnit is not None and dollarsOffPerUnit < 0:
        dollarsOffPerUnit = None

    if dollarsPerUnit is not None and dollarsPerUnit < 0:
        dollarsPerUnit = None

    return (minNumber, discount, dollarsPerUnit, dollarsOffPerUnit)

def detectFree(s):
    return "FREE" in s

def detectHalf(s):
    return "HALF" in s

def detectPercent(s):
    return "%" in s

def detectSave(s):
    return "SAVE" in s

def detectOff(s):
    return "OFF" in s

# Test cases
if __name__ == "__main__":
    print(parsePromo("BUY ONE GET ONE FREE", "SAVE 14 on 2\n"))
    print(parsePromo("HALF OFF HUGE LAWBSTA", "SAVE 12 on 2\n"))
    print(parsePromo("25% OFF", "SAVE $12/lb\n"))
    print(parsePromo(" 10% OFF", "SAVE $10\n"))
    print(parsePromo(" 10% OFF", "SAVE 10\n"))
    print(parsePromo("SAVE 150", ""))
    print(parsePromo("199 OFF", ""))
    print(parsePromo("10/$10", "SAVE 299 on 10"))
    print(parsePromo("10[*10", "SAVE $2 on 10"))
    print(parsePromo("$3.40/lb", "SAVE $2/lb"))
