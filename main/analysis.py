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

"""

import argparse
import json
import wordcloud_helper
from collections import OrderedDict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def video_score(views, likes, dislikes, num_comments):
    """
    Computes an artificial score for a video indicating the video's popularity.

    The current formula in use is:
    (views * 0.1) + (likes) - (dislikes) + (num_comments)

    :param views:
    :param likes:
    :param dislikes:
    :param num_comments:
    :return
    """
    return (views * 0.1) + (likes) - (dislikes) + (num_comments)


def comment_score(likes, replies):
    """
    Computes an artificial score for a comment indicating its rank.
    Note that the dataset does not include dislikes, only likes and replies.

    The current formula in use is:
    (likes * 2) + num_replies

    :param likes:
    :param replies:
    :return:
    """
    return likes * 2 + replies


if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output directory to use", required=True)
    parser.add_argument("-c", "--cat", help="Specify a category id", required=True)
    args = parser.parse_args()

    with open(args.input, "r") as data_file:
        data_entries = json.load(data_file)

        # filter by category
        data_entries = {k: v for (k, v) in data_entries.items() if v["category_id"] == args.cat}

        # sort by video score
        num_videos = 10
        ordered = sorted(data_entries.items(), reverse=True,
                         key=lambda k: video_score(int(k[1]["views"]), int(k[1]["likes"]),
                                                   int(k[1]["dislikes"]), len(k[1]["comments"])))[:num_videos]
        top_videos = OrderedDict(ordered)

        # get the comments for these top videos
        for video_id in top_videos:
            entry = top_videos[video_id]
            comments = entry["comments"]

            # sort by comment score
            num_comments = 20
            ordered_comments = sorted(comments, reverse=True, key=lambda pair: comment_score(int(pair["likes"]), int(pair["replies"])))[:num_comments]

            # tokenize the comments into sentences
            comment_list = map(lambda c: c["comment_text"], ordered_comments)
            full_sentence_list = []
            for comment in comment_list:
                sentences = tokenize.sent_tokenize(comment)
                full_sentence_list.extend(sentences)

            # do the usual: sentiment scores, wordclouds
            sid = SentimentIntensityAnalyzer()
            for sentence in full_sentence_list:
                print(sentence)
                ss = sid.polarity_scores(sentence)
                for k in sorted(ss):
                    print('{0}: {1}, '.format(k, ss[k]), end='')
                    print()

        # test
        """
        for key in data_entries:
            views = int(data_entries[key]["views"])
            likes = int(data_entries[key]["likes"])
            dislikes = int(data_entries[key]["dislikes"])
            num_comments = len(data_entries[key]["comments"])
            print("score %s" % (views + (likes * 2) - (dislikes * 2)))

        for key in top_videos:
            views = int(top_videos[key]["views"])
            likes = int(top_videos[key]["likes"])
            dislikes = int(top_videos[key]["dislikes"])
            num_comments = len(top_videos[key]["comments"])
            print("score %s" % (views + (likes * 2) - (dislikes * 2)))
        """


