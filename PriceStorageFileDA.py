import csv


class PriceStorageDA:

    def savePrice(self, time, product_code, price):
        filename = "prices.csv"

        row = [time, product_code, price]
        with open(filename, 'a+') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)

    def getPrices(self, product_code):
        filename = "prices.csv"

        rows = []
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                # Add row to response if the row isn't empty.
                if row:
                    rows.append(row)
        return rows