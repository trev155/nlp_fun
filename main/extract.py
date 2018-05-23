"""
extract.py

Objective of this file is to read input data and output it all into a file that is easier to parse.
"""

import argparse
import os
import json

from extract_helpers import extract_video_data, extract_categories_data, parse_comments_data

DATA_DIR = "data"

def preprocess(comments_csv, videos_csv, categories_json):
    """
    Preprocessing input files.

    :param comments_csv: string, filename
    :param videos_csv: string, filename
    :param categories_json: string, filename
    :return:
    """
    with open(comments_csv, "r") as comments_file, \
            open(videos_csv, "r") as videos_file, \
            open(categories_json, "r") as categories_file:
        video_data = extract_video_data(videos_file)
        categories_data = extract_categories_data(categories_file)
        all_data = parse_comments_data(video_data, categories_data, comments_file)
    return all_data


if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input set to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output file name to use", required=True)
    args = parser.parse_args()

    # Construct input file names
    comments_filename = None
    videos_filename = None
    categories_filename = None

    if args.input == "US":
        comments_filename = "UScomments.csv"
        videos_filename = "USvideos.csv"
        categories_filename = "US_category_id.json"
    elif args.input == "GB":
        comments_filename = "GBcomments.csv"
        videos_filename = "GBvideos.csv"
        categories_filename = "GB_category_id.json"
    else:
        print("Mode invalid: Valid modes = 'US', 'GB'")
        exit(1)

    comments_csv_file = os.path.join(os.getcwd(), DATA_DIR, comments_filename)
    videos_csv_file = os.path.join(os.getcwd(), DATA_DIR, videos_filename)
    categories_json_file = os.path.join(os.getcwd(), DATA_DIR, categories_filename)

    # Run preprocessing
    data = preprocess(comments_csv_file, videos_csv_file, categories_json_file)

    # Write out data to file
    with open(args.output, "w") as outfile:
        json.dump(data, outfile)

    exit(0)
