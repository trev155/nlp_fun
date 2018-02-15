"""
preprocessing.py

Objective of this file is to read inputs from a .csv file, preprocess and clean up the data, and write the results
back out into a separate json file.


"""
import argparse


CSV_FILE = "CAvideos.csv"
JSON_FILE = "CA_category_id.json"


def preprocess(input_file, output_file, num_lines):
    """
    Preprocess the input CSV file.
    Takes num_lines lines from the input file. For each line, clean up the data and tag it with spaCy.
    Write out all the preprocessed lines back out to the JSON file specified by the output_file.

    :param input_file:
    :param output_file:
    :param num_lines:
    :return:
    """
    with open(CSV_FILE, "r") as input_file:
        print(input_file.readline())
        print(input_file.readline())

    return 0


if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file name to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output file name to use", required=True)
    parser.add_argument("-n", help="Specify the amount of lines to read from the CSV file", default=10)
    args = parser.parse_args()

    # Run preprocessing
    data = preprocess(args.input, args.output, args.n)

    exit(0)
