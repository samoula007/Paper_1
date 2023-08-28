import csv
import random

def generate_dummy_offers(num_rows):
    data = []
    for _ in range(num_rows):
        cost = round(random.uniform(10.00, 100.00), 2)
        num_offers = random.randint(1, 10)
        data.append((cost, num_offers))
    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["cost", "num"])
        for row in data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    num_rows = 10
    offer_data = generate_dummy_offers(num_rows)
    csv_filename = "data/offers.csv"
    write_to_csv(offer_data, csv_filename)
    print(f"{num_rows} rows of offer data have been generated and saved to {csv_filename}.")
