class AdBlockData():
    def __init__(self):
        self.flyer_name = ""
        self.product_name = ""
        self.unit_promo_price = None # Number
        self.uom = ""
        self.least_unit_for_promo = None # Number
        self.save_per_unit = None # Number
        self.discount = None # Number
        self.organic = False
        self.confidence = 0


    def createFromCsvRow(row):
        data = AdBlockData()
        data.flyer_name = row[0]
        data.product_name = row[1]
        data.unit_promo_price = row[2]
        data.uom = row[3]
        data.least_unit_for_promo = row[4]
        data.save_per_unit = row[5]
        data.discount = row[6]
        data.organic = row[7]
