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

NOTE:
- the youtube comment extract API is not good (see the comments on the kaggle page)
- as a result, the top comments may not be fully accurate

As usual, a data entry looks like:
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
import wordcloud_helper
from collections import OrderedDict
from nltk.sentiment.vader import SentimentIntensityAnalyzer


##########
# Scores #
##########
def video_score(views, likes, dislikes, num_comments):
    """
    Computes an artificial score for a video indicating the video's popularity.

    The current formula in use is:
    views + (likes * 10) - (dislikes * 10) + (num_comments * 10)

    :param views: int, number of views on a video
    :param likes: int, number of likes on a video
    :param dislikes: int, number of dislikes on a video
    :param num_comments: int, number of comments on the video
    :return: float, comment score
    """
    return views + (likes * 10) - (dislikes * 10) + (num_comments * 10)


def comment_score(likes, replies):
    """
    Computes an artificial score for a comment indicating its rank.
    Note that the dataset does not include dislikes, only likes and replies.

    The current formula in use is:
    (likes * 2) + num_replies

    :param likes: int, number of likes on a comment
    :param replies: int, number of replies on a comment
    :return: int, comment score
    """
    return (likes * 2) + replies


########
# Flow #
########
def run(input_path, output_path, category_id):
    # load data
    with open(input_path, "r") as data_file:
        data_entries = json.load(data_file)

    # these will hold the positive and negative comments from the top videos
    positive_comments = []
    negative_comments = []

    # filter by category
    data_entries = {k: v for (k, v) in data_entries.items() if v["category_id"] == category_id}
    # get top videos
    top_videos = filter_top_videos(data_entries, 10)

    # iterate over each of the top videos
    for video_id in top_videos:
        # get the top comments for the video
        entry = top_videos[video_id]
        video_comments = entry["comments"]
        video_top_comments = filter_top_comments(video_comments, 20)

        # compute the sentiment scores for each comment
        sentiment_entries = compute_sentiment_entries(video_top_comments)

        # sort the sentiment scores
        sentiment_entries = sorted(sentiment_entries, reverse=True, key=lambda score: score[1]["compound"])

        # print out the comments and the sentiment scores
        # accumulation of positive / negative comments
        print("_" * 80)
        print("[VIDEO: %s] by [CHANNEL: %s]" % (entry["title"], entry["channel_title"]))
        print("Views: %s, Likes: %s, Dislikes: %s, Num. Replies: %s" % (entry["views"], entry["likes"], entry["dislikes"], len(entry["comments"])))
        print("_" * 80)
        for sentiment_entry in sentiment_entries:
            comment = sentiment_entry[0]
            score = sentiment_entry[1]

            if score["compound"] > 0.3:
                positive_comments.append(comment)
            elif score["compound"] < -0.3:
                negative_comments.append(comment)

            print(comment)
            print(score)
            print("")

    # post processing - generate wordclouds
    positive_wc_text = " ".join(positive_comments)
    positive_wc_name = category_id + "-" + "positive"
    wordcloud_helper.generate_wordcloud(positive_wc_text, positive_wc_name, output_path)

    negative_wc_text = " ".join(negative_comments)
    negative_wc_name = category_id + "-" + "negative"
    wordcloud_helper.generate_wordcloud(negative_wc_text, negative_wc_name, output_path)


def filter_top_videos(data_entries, num_videos):
    """
    Get the top videos from the data entries. Videos are scored according to the video_score() function.

    :param data_entries: dict, of {video id: video data}
    :param num_videos: int, number of videos to return
    :return: dict, of {video id: video data}, of size num_videos
    """
    ordered = sorted(data_entries.items(), reverse=True,
                     key=lambda k: video_score(int(k[1]["views"]), int(k[1]["likes"]),
                                               int(k[1]["dislikes"]), len(k[1]["comments"])))[:num_videos]
    top_videos = OrderedDict(ordered)
    return top_videos


def filter_top_comments(comments, num_comments):
    """
    Get the top comments from a list of comments. Videos are scored according to the comment_score() function.

    :param comments: list of comment entries
    :param num_comments: int, number of comments to return
    :return: list of strings, each element representing a sentence from a comment
    """
    ordered_comments = sorted(comments, reverse=True,
                              key=lambda pair: comment_score(int(pair["likes"]), int(pair["replies"])))[
                       :num_comments]
    comment_list = list(map(lambda c: c["comment_text"], ordered_comments))
    return comment_list


def compute_sentiment_entries(comment_sentences):
    """
    Compute sentiment scores for each sentence in comment_sentences.
    Uses NLTK/Vader, which returns a structure of {"compound": score, "pos": score, "neg": score, "neu": score}.
    Returns a list of tuples, (sentence, sentiment score dict).

    :param comment_sentences: list of strings
    :return: list of tuples, (sentence, sentiment score dict)
    """
    all_sentiment_scores = []
    sid = SentimentIntensityAnalyzer()
    for sentence in comment_sentences:
        ss = sid.polarity_scores(sentence)
        all_sentiment_scores.append((sentence, ss))
    return all_sentiment_scores


########
# MAIN #
########
if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output directory to use", required=True)
    parser.add_argument("-c", "--cat", help="Specify a category id", required=True)
    args = parser.parse_args()

    run(args.input, args.output, args.cat)
