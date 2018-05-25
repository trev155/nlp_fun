# nlp_fun
Working with the "Trending Youtube Statistics" dataset, found on: https://www.kaggle.com/datasnaek/youtube/data

Point of this is to dabble into analyzing data. It's simple for sure - i'm not doing anything revolutionary, mostly just processing data and running it through some NLP libraries.

## Run
Uses python3.
Have to install these packages: wordcloud, nltk

1. run extract.py script (reads original data from files, combines them, preprocesses the comments a bit, outputs them into a .json)
`python3 main/extract.py -s US -o output/preprocUS.json`
- this will read in the US files, and generate an output file at `output/preprocUS.json`

`python3 main/extract.py -s GB -o output/preprocGB.json`
- this will read in the GB files, and generate an output file at `output/preprocGB.json`

Tests:
`python3 main/extract_helpers_test.py`

2. List videos metadata.
Lists all video metadata (likes, views, category, etc) for all videos.

`python3 main/video_list.py -i output/preprocUS.json`

2a. Generate wordclouds by category id.
`python3 main/wordcloud_by_category.py -i output/preprocUS.json -o output/wordcloudsUS -s US -c 24`
- this will generate a wordcloud for all of the comments of all of the videos that are in category id 24 (Entertainment), for US videos.
- to see the list of category ids, look at the `*_category_id.json` files (in the `data` directory).
- some categories don't have videos

`python3 main/wordcloud_by_category.py -i output/preprocUS.json -o output/wordcloudsUS -s US`
- this will go through every category and generate a wordcloud for all comments for that category

2b. Generate wordclouds by video id.
A variant of 2a, where we generate a wordcloud for a specific video id.

Example:
`python3 main/wordcloud_by_id.py -i output/preprocUS.json -o output/wordcloudsUS -v ckXN4Tc6-c8`

This will generate a wordcloud file, `ckXN4Tc6-c8.png` in `output/wordcloudUS`.

3. Sentiments and wordclouds, by category id.
A variant of 2a, where I go through all the videos of a specific category id.
Then, I use nltk/vader to get the sentiment score of each comment, each video in that category.
I separate comments based on if they have positive or negative sentiment.
Then, I generate a wordcloud for all the positive comments, and a wordcloud for all the negative comments.

`python3 main/sentiments.py -i output/preprocUS.json -o output/wordcloudsUS -s US -c 25`

## TODOs
- more complex analytics, eg) get the top 10 comments (in terms of likes/dislikes ratio) for each of the top 10 videos for a specific category, and make a wordcloud for these comments