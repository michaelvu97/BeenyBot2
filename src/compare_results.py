import csv

def csvToData(path):
    results_data = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == "flyer_name":
                continue
            results_data.append(AdBlockData.createFromCsvRow(row))

    return results_data

def compareResults(flyer_name, results_path, true_results_path):

    our_results = csvToData(results_path)
    true_results = csvToData(true_results_path)

    # Find things that we got correct
    for prediction in our_results:
        matching_result = [thing in true_results if thing.product_name == prediction.product_name]
        if len(matching_result) == 0:
            matching_result = None
            print("False positive result: " + prediction.product_name)
            continue


        matching_result = matching_result[0]
        # TODO the rest


