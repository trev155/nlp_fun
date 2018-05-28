"""
wordcloud_helper.py

Main functionality to generate a wordcloud.
(uses the library from amueller, https://github.com/amueller/word_cloud)
"""
from wordcloud import WordCloud, STOPWORDS
import os


def construct_stopwords():
    """
    The default STOPWORDS does not include certain swear words that I would like to exclude.
    Make sure to return a set of strings, as that is what is needed for the WordCloud library.

    :return: set of strings
    """
    extra_words_to_exclude = [
        "cunt",
        "faggot",
        "fag",
        "nigger",
        "nigga",
        "nugger",
        "nugga"
    ]

    new_stopwords = STOPWORDS
    for word in extra_words_to_exclude:
        STOPWORDS.add(word)
    return new_stopwords


def generate_wordcloud(text, name, output_dir):
    """
    Generate a word cloud, given text.

    :param text: str, tokens have to be space-separated
    :param name: str, filename to output
    :param output_dir: str, output directory name
    """
    wc = WordCloud(background_color="white", width=700, height=500, collocations=False, max_words=150,
                   stopwords=construct_stopwords())
    wc.generate(text)
    wc.to_file(os.path.join(output_dir, name) + ".png")
