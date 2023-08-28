import csv
import random

def generate_dummy_customers(num_rows):
    data = []
    for _ in range(num_rows):
        p = round(random.uniform(30.00, 1000.00), 2)
        alpha = round(random.uniform(0.00, 1.00), 2)
        gamma = round(random.uniform(0.00, 1.00), 2)
        data.append((p, alpha, gamma))
    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["p", "alpha", "gamma"])
        for row in data:
            csv_writer.writerow(row)

if __name__ == "__main__":
    num_rows = 100
    dummy_data = generate_dummy_customers(num_rows)
    csv_filename = "data/customers.csv"
    write_to_csv(dummy_data, csv_filename)
    print(f"{num_rows} rows of dummy data have been generated and saved to {csv_filename}.")
