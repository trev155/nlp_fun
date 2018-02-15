import json
import csv
import numpy as np

CSV_FILE = "CAvideos.csv"
JSON_FILE = "CA_category_id.json"


def do_stuff():
    """
    Returns a numpy array of all the data.
    :return:
    """
    data = []

    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

    return data

if __name__ == "__main__":
    data = do_stuff()
    exit(0)


