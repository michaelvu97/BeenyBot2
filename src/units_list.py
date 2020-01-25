import csv 

units_list = []
with open("units_dictionary.csv", "r", encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        units_list.append(row[0].lower())

    units_list.remove("units")

    # TODO remove the first?

def getUnitsList():
    return units_list

