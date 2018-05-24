"""
wordcloud_by_category.py

Generates a wordcloud for each category id.

Input file comes from the output of extract.py, which generates a .json file with data entries.
Format of a data entry:
{
    video_id: {
        "title": title,
        "channel_title": channel_title,
        "category_id": category_id,
        "category_name": category_name,
        ...
        "comments": [
            {
                "comment_text": comment_text,
                "likes": likes,
                "replies": replies
            }
        ]
    }
}

"""

import argparse
import json
import extract_helpers
import wordcloud_helper

###########
# GLOBALS #
###########
CATEGORY_DATA = "data/US_category_id.json"


###########
# HELPERS #
###########
def wordcloud_for_specific_category_id(input_filename, output_dir, category_id):
    """
    Generate a word cloud for the category_id.

    :param input_filename: string, the filename of the input data file
    :param output_dir: string, the name of the output dir
    :param category_id: string, category id
    """
    print("Starting: Generate a word cloud for category id (%s)" % category_id)

    with open(input_filename, "r") as input_file:
        all_data_entries = json.load(input_file)

        # get all videos with specified category
        relevant_data_entries = {k:v for (k,v) in all_data_entries.items() if v["category_id"] == category_id}

        if len(relevant_data_entries) == 0:
            print("There were no videos for this category, continuing")
            return

        # prepare to generate a word cloud
        word_counts = get_token_counts(relevant_data_entries)
        counts_text = counts_to_text(word_counts)
        output_filename = category_id + "-" + category_data[category_id]

        # generate the word cloud
        wordcloud_helper.generate_wordcloud(counts_text, output_filename, output_dir)


def get_token_counts(data_entries):
    """
    Go through all the data entries in data. Each data entry represents a single video.
    Count the occurrences of every token/word.

    :param data_entries: dictionary of data entries
    :return: dictionary of {token: count}
    """
    counts = {}
    # Iterate over all data entries
    for video_id in data_entries:
        # Iterate over all the comments for this data entry
        entry = data_entries[video_id]
        for comment in entry["comments"]:
            comment_text = comment["comment_text"]
            comment_split = comment_text.split()
            for word in comment_split:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
    return counts


def counts_to_text(counts):
    """
    Given a dictionary of the format,
    {
        "token": count
    }
    return a space-separated string representing the dictionary's token counts.

    Example:
    {"hello": 2, "hey": 1, "apple": 2}
    should result in,
    "hello hello hey apple apple"

    :param counts: dictionary of {token: count}
    :return: string
    """
    str_list = []
    for token in counts:
        token_count = counts[token]
        for i in range(token_count):
            str_list.append(token)
    return " ".join(str_list)


if __name__ == "__main__":
    # Preliminary parsing - get category id and names
    with open(CATEGORY_DATA, "r") as category_file:
        category_data = extract_helpers.extract_categories_data(category_file)

    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output directory to use", required=True)
    parser.add_argument("-c", "--cat", help="Category id to generate wordclouds for", required=False)
    args = parser.parse_args()

    # If command line argument contains -c option, only generate a word cloud for that category id.
    # If -c option not provided, generate a word cloud for every category id.
    if args.cat is not None:
        wordcloud_for_specific_category_id(args.input, args.output, args.cat)
    else:
        for cat_id in category_data:
            wordcloud_for_specific_category_id(args.input, args.output, cat_id)
