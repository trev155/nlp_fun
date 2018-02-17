import csv
import json


###################
# Data Extraction #
###################
def extract_video_data(videos_file):
    """
    Extract video data.

    Video data is in the form of:
    {
        "video_id": {
            "title": title,
            "channel_title": channel_title,
            ...
        }
    }
    :param videos_file: file handler
    :return: dictionary of {str, video_data}
    """
    videos_data = {}
    for i, line in enumerate(videos_file):
        if i == 0:
            continue

        # Parse line
        line = line.strip()
        fields = separate_csv_line(line)
        video_id = fields[0]
        title = fields[1]
        channel_title = fields[2]
        category_id = fields[3]
        tags = fields[4]
        views = fields[5]
        likes = fields[6]
        dislikes = fields[7]
        comment_total = fields[8]
        thumbnail_link = fields[9]
        date = fields[10]

        videos_data[video_id] = {
            "title": title,
            "channel_title": channel_title,
            "category_id": category_id,
            "tags": tags,
            "views": views,
            "likes": likes,
            "dislikes": dislikes,
            "comment_total": comment_total,
            "thumbnail_link": thumbnail_link,
            "date": date
        }
    return videos_data


def extract_categories_data(categories_file):
    """
    Extract categories data.

    The category data looks like:
    {
        "category_id": "category_name
    }
    :param categories_file: file handle
    :return: dictionary
    """
    categories_data = {}
    data = json.load(categories_file)
    items = data["items"]
    for item in items:
        category_id = item["id"]
        category_name = item["snippet"]["title"]
        categories_data[category_id] = category_name
    return categories_data


def parse_comments_data(videos_data, categories_data, comments_file):
    """
    Parse comments.
    Requires having the videos_data and categories_data available, so that we can combine all the data from these
    different files in one step.

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
    :param videos_data: dictionary of
    :param categories_data: dictionary of
    :param comments_file: file handle
    :return:
    """
    all_data = {}
    for i, line in enumerate(comments_file):
        if i == 0:
            continue

        # Parse line
        line = line.strip()
        try:
            fields = separate_csv_line(line)
            video_id = fields[0]
            comment_text = fields[1]
            likes = fields[2]
            replies = fields[3]
        except Exception as e:
            # There are a bunch of exceptions that will come up due to bad input data. Simply skip these entries
            print("warning: exception encountered when parsing the comments file", e)
            continue

        comment_entry = {
            "comment_text": comment_text,
            "likes": likes,
            "replies": replies
        }
        # If video_id of this comment already exists in the dictionary, add the comment to its comment list
        if video_id in all_data:
            all_data[video_id]["comments"].append(comment_entry)
        # Otherwise, create a new entry - make sure to fetch the appropriate video and category data
        else:
            video_data = {
                "title": videos_data[video_id]["title"],
                "channel_title": videos_data[video_id]["channel_title"],
                "category_id": videos_data[video_id]["category_id"],
                "category_name": categories_data[videos_data[video_id]["category_id"]],
                "tags": videos_data[video_id]["tags"],
                "views": videos_data[video_id]["views"],
                "likes": videos_data[video_id]["likes"],
                "dislikes": videos_data[video_id]["dislikes"],
                "comment_total": videos_data[video_id]["comment_total"],
                "thumbnail_link": videos_data[video_id]["thumbnail_link"],
                "date": videos_data[video_id]["date"],
                "comments": [comment_entry]
            }
            all_data[video_id] = video_data

    return all_data


###########
# Utility #
###########
def separate_csv_line(s):
    """
    Split a line of a csv file.
    Returns a list of the fields of the string s.

    Examples:
    'hello,world,123,456' -> ['hello', 'world', '123', '456']
    '"hi,hey",123,"ha,hi,he",456' -> ['hi,hey', '123', 'ha,hi,he', '456']

    :param s: string, a line of some csv file
    :return: list of strings
    """
    reader = csv.reader(s.splitlines(), delimiter=",")
    fields = list(reader)[0]
    return fields

