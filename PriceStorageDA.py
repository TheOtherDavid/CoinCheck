import csv


class PriceStorageDA:

    def savePrice(self, time, product_code, price):
        filename = "prices.csv"

        row = [time, product_code, price]
        with open(filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)

