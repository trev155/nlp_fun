"""
wordcloud_by_id.py

2 options
- if you provide the -l option, the script outputs a list of video ids and titles to use.
- if you don't provide the -l option, you have to provide the -v option and specify a video id.

A wordcloud is generated for all of the comments for that video id.
"""

import argparse
import json
import wordcloud_helper

DATA_DIR = "data"

if __name__ == "__main__":
    # Command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify the input file to use", required=True)
    parser.add_argument("-o", "--output", help="Specify the output directory to use", required=True)
    parser.add_argument("-l", "--list", help="List video ids.", required=False, action="store_true")
    parser.add_argument("-v", "--videoId", help="The video id to use", required=False)
    args = parser.parse_args()

    if args.list:
        with open(args.input, "r") as data_file:
            data_entries = json.load(data_file)
            for video_id in data_entries:
                entry = data_entries[video_id]
                print("video id: %s, video title: %s, channel title: %s, views: %s, likes: %s, "
                      "dislikes: %s, category_id: %s" % (video_id, entry["title"],
                                                         entry["channel_title"], entry["views"],
                                                        entry["likes"], entry["dislikes"], entry["category_id"]))

    if args.videoId:
        with open(args.input, "r") as data_file:
            data_entries = json.load(data_file)
            data_entry = {k: v for (k, v) in data_entries.items() if k == args.videoId}

            if len(data_entry) == 0:
                print("Video id (%s) not found. Nothing happened." % args.videoId)
                exit(0)

            entry = data_entry[args.videoId]

            # count all the words for all the comments of this video
            counts = {}
            for comment in entry["comments"]:
                comment_text = comment["comment_text"]
                tokens = comment_text.split()
                for token in tokens:
                    if token in counts:
                        counts[token] += 1
                    else:
                        counts[token] = 1

            # construct a string out of the counts
            str_list = []
            for token in counts:
                for i in range(counts[token]):
                    str_list.append(token)

            wordcloud_text = " ".join(str_list)
            wordcloud_helper.generate_wordcloud(wordcloud_text, args.videoId, args.output)

            # some print output
            print("Generated a wordcloud for video id (%s) at (%s/%s)" % (args.videoId, args.output, args.videoId))
            print("video id: %s, video title: %s, channel title: %s, views: %s, likes: %s, "
                  "dislikes: %s, category_id: %s" % (args.videoId, entry["title"],
                                                     entry["channel_title"], entry["views"],
                                                     entry["likes"], entry["dislikes"], entry["category_id"]))

    if not args.list and not args.videoId:
        print("No -l option or -v option specified. Nothing happened.")
