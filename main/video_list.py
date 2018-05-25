"""
video_list.py

A script that prints out all video metadata.
"""
import argparse
import json
from collections import OrderedDict

if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    args = parser.parse_args()

    with open(args.input, "r") as data_file:
        data_entries = json.load(data_file)

        # Below: sorting the dictionary of data entries by category id and views
        ordered = sorted(data_entries.items(), key=lambda x: (int(x[1]["category_id"]), -int(x[1]["views"])))
        ordered_entries = OrderedDict(ordered)

        for video_id in ordered_entries:
            entry = data_entries[video_id]
            print("%s %s +%s -%s (%s - %s) [%s - %s]" % (video_id, entry["views"], entry["likes"],
                                                       entry["dislikes"], entry["category_id"],
                                                       entry["category_name"], entry["title"],
                                                       entry["channel_title"]))
