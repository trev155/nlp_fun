"""
sentiments.py

Perform sentiment analysis on individual videos (within a category, since there are many videos).

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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


CATEGORY_DATA = "data/US_category_id.json"


def extract_sentiments(comments):
    """
    Print sentiment data for this video's comments.

    Returns a tuple of 3 elements:
    - sentiment_score: a value indicating the average sentiment of all of these comments
    - positive_comments: list of strings, the comments which had positive sentiment score
    - negative_comments: list of strings, the comments which had negative sentiment score

    A comment entry looks like:
    "comments": [
        {
            "comment_text": comment_text,
            "likes": likes,
            "replies": replies
        }
    ]
    :param comments: list of comment entries
    :return: tuple of (sentiment score, positive comments, negative comments)
    """
    positive_comments = []
    negative_comments = []
    all_comment_scores = []

    for comment in comments:
        # use the nltk tokenizer to split the comment text into sentences
        comment_text = comment["comment_text"]
        sentences = tokenize.sent_tokenize(comment_text)

        # get compound scores (sentiments) for each sentence in this comment
        sid = SentimentIntensityAnalyzer()
        compound_scores = []
        for sentence in sentences:
            ss = sid.polarity_scores(sentence)
            compound_score = ss["compound"]
            compound_scores.append(compound_score)

        if len(compound_scores) == 0:
            # implies that there were no comments for this video, which is totally possible if comments disabled
            continue

        avg_compound_score = sum(compound_scores) / len(compound_scores)
        if avg_compound_score >= 0:
            positive_comments.append(comment_text)
        else:
            negative_comments.append(comment_text)

        all_comment_scores.append(avg_compound_score)

    sentiment_score = sum(all_comment_scores) / len(all_comment_scores)
    return sentiment_score, positive_comments, negative_comments


def sentiments_by_category_id(input_filename, output_dir, category_id):
    """
    Get sentiments by category id.
    Read input from input_file.
    Output any data to output_dir.

    For each video, find its sentiment score and print out its metadata (likes, dislikes, views, etc).

    Generate wordclouds for both the positive comments and the negative comments of this

    :param input_filename: string, the name of the input data file
    :param output_dir: string, name of output directory
    :param category_id: string, category id.
    """
    print("Starting: Sentiments for category id (%s)" % category_id)

    with open(input_filename, "r") as input_file:
        all_data_entries = json.load(input_file)

        # get all videos with specified category

        relevant_data_entries = {k: v for (k, v) in all_data_entries.items() if v["category_id"] == category_id}

        if len(relevant_data_entries) == 0:
            print("There were no videos for this category, continuing")
            return

        # iterate over each video, perform sentiment analysis and print out data
        positive_comments = []
        negative_comments = []
        for video_id in relevant_data_entries:
            print("Processing video id: (%s)" % video_id)
            entry = relevant_data_entries[video_id]
            score, positive, negative = extract_sentiments(entry["comments"])
            positive_comments.extend(positive)
            negative_comments.extend(negative)

            print("Video title: %s, Views: %s, Likes: %s, Dislikes: %s, Channel title: %s, "
                  "Compound sentiment score: %0.4f" % (entry["title"],
                  entry["views"], entry["likes"], entry["dislikes"], entry["channel_title"], score))
            print("_" * 20)

        # generate wordclouds
        pos_name = category_id + "-" + category_data[category_id] + "-" + "positive"
        wordcloud_helper.generate_wordcloud(" ".join(positive_comments), pos_name, output_dir)

        neg_name = category_id + "-" + category_data[category_id] + "-" + "negative"
        wordcloud_helper.generate_wordcloud(" ".join(negative_comments), neg_name, output_dir)


if __name__ == "__main__":
    # Preliminary parsing - get category id and names
    with open(CATEGORY_DATA, "r") as category_file:
        category_data = extract_helpers.extract_categories_data(category_file)

    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output directory to use", required=True)
    parser.add_argument("-c", "--cat", help="Category id to generate wordclouds for", required=True)
    args = parser.parse_args()

    sentiments_by_category_id(args.input, args.output, args.cat)
