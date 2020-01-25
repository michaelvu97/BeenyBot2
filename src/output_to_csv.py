import csv
from ad_block_data import AdBlockData

def fmtPrice(price):
    if price is None:
        return ""

    return "{:.2f}".format(price).rstrip('0').rstrip('.')

def fmtBool(boolguy):
    if (boolguy):
        return "1"
    return "0"

def numToString(num):
    if num is None:
        return ""
    return str(num)

def outputToCsv(adBlockDataList, fileName = "output.csv"):
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["flyer_name","product_name","unit_promo_price","uom","least_unit_for_promo","save_per_unit","discount","organic"])
        for adBlockData in adBlockDataList:
            writer.writerow([
                adBlockData.flyer_name, 
                adBlockData.product_name, 
                fmtPrice(adBlockData.unit_promo_price),
                adBlockData.uom,
                numToString(adBlockData.least_unit_for_promo),
                fmtPrice(adBlockData.save_per_unit),
                fmtPrice(adBlockData.discount),
                fmtBool(adBlockData.organic)
                ])

if __name__ == "__main__":
    # Tests

    abdList = []

    abd = AdBlockData()
    abd.flyer_name = "week_1_page_1"
    abd.product_name = "Blueberries"
    abd.unit_promo_price = 2.5
    abd.uom = "lb"
    abd.least_unit_for_promo = 10
    abd.save_per_unit = 3.49
    abd.discount = 0.2
    abd.organic = False

    abdList.append(abd)

    abd = AdBlockData()
    abd.flyer_name = "week_1_page_2"
    abd.product_name = "Blueberries"
    abd.unit_promo_price = 1
    abd.uom = "0.25 lb"
    abd.least_unit_for_promo = 2
    abd.save_per_unit = None
    abd.discount = 0.25
    abd.organic = True

    abdList.append(abd)

    outputToCsv(abdList)
