"""
File: lyric_parsers.py
Description: contains parser functions for different filetypes
"""

import json
import re
import string
from collections import Counter

def json_parser(lyric, filename):
    # read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)

    # iterate over each song
    words = [] # initialize list of words
    for song in data['songs']:
        # grab lyrics from each song
        lyrics = song['lyrics']
        
        # remove fluff upto and including first "Lyrics"
        cleaned_lyrics = re.sub(r'\d+ .*? Lyrics', '', lyrics)

        # remove "Embed" at the end
        cleaned_lyrics = re.sub(r'Embed$', '', cleaned_lyrics)

        # clean up lyrics
        cleaned_lyrics = cleaned_lyrics.strip().lower()
        cleaned_lyrics = cleaned_lyrics.translate(str.maketrans('', '', string.punctuation))

        # add song's lyrics to word mass
        words += cleaned_lyrics.split()

    # remove stop words
    filtered_words = [word for word in words if word not in lyric.data["stop_words"]]

    # calculate word count and number of words
    results = {
        'wordcount': Counter(filtered_words),
        'numwords' : len(filtered_words)
    }

    return results
