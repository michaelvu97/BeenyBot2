import csv 

products_list = []
with open("product_dictionary.csv", "r", encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if (row[0] == "CrÃ¨me Cookies"):
            continue
        products_list.append(row[0].lower())

    products_list.remove("product_name")

    # TODO remove the first?

def getProductsList():
    return products_list

