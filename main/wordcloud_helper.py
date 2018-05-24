"""
wordcloud.py

Main functionality to generate a wordcloud.
(uses the library from amueller, https://github.com/amueller/word_cloud)
"""
from wordcloud import WordCloud
import os


def generate_wordcloud(text, name, output_dir):
    """
    Generate a word cloud, given text.

    :param text: str, tokens have to be space-separated
    :param name: str, filename to output
    :param output_dir: str, output directory name
    """
    wc = WordCloud(background_color="white", width=800, height=600, collocations=False)
    wc.generate(text)
    wc.to_file(os.path.join(output_dir, name) + ".png")