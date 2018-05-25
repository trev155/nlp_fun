"""
analysis.py

A script that does a bit more in-depth analysis on the data.

Idea:
- given a category id,
- for the top X videos (by likes, dislikes, views, number of comments)
- get the top X comments (by likes / dislikes)
- compute the sentiment score for these comments
- generate a wordcloud for these comments

- perhaps repeat the process, but for the bottom X videos / comments

Other questions to investigate (these can be done in other scripts):
- Is there a relationship between the top comments for a video, and its sentiment?
- Is there a relationship between likes/dislikes ratio and comment sentiment?
- etc.

"""

import argparse
import json
import wordcloud_helper
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output directory to use", required=True)
    args = parser.parse_args()

    with open(args.input, "r") as data_file:
        data_entries = json.load(data_file)

        pass
