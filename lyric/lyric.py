"""
File: lyric.py
Description: a reusable library for lyric text analysis and comparison
"""

import matplotlib.pyplot as plt
import random as rnd
from collections import Counter, defaultdict
import string
from wordcloud import WordCloud
import numpy as np
from textblob import TextBlob
import re
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd

class Lyric:
    def __init__(self):
        """ constructor """
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(lyric, filename):
        """ default text parser for unformatted text files """
        with open(filename, "r") as f:
            text_file = f.read()

        # remove white space
        text_file = text_file.strip()

        # convert to lowercase
        text_file = text_file.lower()

        # remove punctuation
        text_file = text_file.translate(str.maketrans('', '', string.punctuation))

         # split into words
        words = text_file.split()

        # remove stop words
        filtered_words = [word for word in words if word not in lyric.data["stop_words"]]

        results = {
            'wordcount': Counter(filtered_words),
            'numwords' : len(filtered_words)
        }

        # print(f"Parsed: {filename}: {results}")

        return results

    def load_text(self, filename, label=None, parser=None):
        """ registers a text file with the library """
        if parser is None:
            results = Lyric._default_parser(self, filename)
        else:
            results = parser(self, filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def load_stop_words(self, stopfile):
        """ load stop words """
        with open(stopfile, "r") as f:
            self.data["stop_words"] = f.read().splitlines()

    def wordcount_sankey(self, word_list=None, k=10):
        """  
        generates and pots sankey diagram connecting texts to common words
        """
        # if no word list is provided:
        # take the k most common words from the union of all texts
        if word_list is None: 
            word_count_union = Counter()
            for text in self.data["wordcount"]:
                word_count_union.update(self.data["wordcount"][text])
            word_list = word_count_union.most_common(k)

        # define nodes
        source_nodes = list(self.data["wordcount"].keys()) # list of text names (strings)
        target_nodes = [word for word, _ in word_list] # list of words (strings)

        # get list of source, target, value dictionaries
        links = []
        for source in source_nodes:
            for target in target_nodes:
                # grab the value for the connection between source and target
                count = self.data["wordcount"][source].get(target, 0) # value (integer)
                links.append({'source': source, 'target': target, 'value': count})

        # create list of unique labels for sources and targets
        node_labels = list(set(source_nodes + target_nodes))

        # map labels (text1, text2, text3) to index values (0, 1, 2)
        node_indices = {label: index for index, label in enumerate(node_labels)}
        link_indices = {
            'source': [node_indices[link['source']] for link in links],
            'target': [node_indices[link['target']] for link in links],
            'value': [link['value'] for link in links]
        }

        # establish links and nodes to be plotted
        link = {'source': link_indices['source'], 'target': link_indices['target'], 'value': link_indices['value']}
        node = {'label': node_labels, 'pad': 50, 'thickness': 50}

        # plot sankey
        sk = go.Figure(data=[go.Sankey(link=link, node=node)])
        sk.show()

    def wordcount_wordcloud(self):
        """
        Generate word clouds for word count data and display them in subplots.
        """
        # Get the word count data
        wordcount_data = self.data["wordcount"]
        num_texts = len(wordcount_data)

        # Calculate the number of rows and columns for subplots
        num_rows = (num_texts + 4) // 5  # Ensure at least 5 plots per row
        num_cols = min(num_texts, 5)

        # Set figure size
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(3 * num_cols, 3 * num_rows))

        # Iterate over each text
        for idx, (label, word_counts) in enumerate(wordcount_data.items()):
            # Calculate subplot indices
            row_idx = idx // num_cols
            col_idx = idx % num_cols

            # Generate word cloud
            wordcloud = WordCloud(width=400, height=400, background_color='white').generate_from_frequencies(
                word_counts)

            # display word cloud in the appropriate subplot
            if num_texts == 1:
                axes.imshow(wordcloud, interpolation="bilinear")
                axes.set_title(f"{label}: Wordcloud")
                axes.axis("off")
            else:
                axes[row_idx, col_idx].imshow(wordcloud, interpolation="bilinear")
                axes[row_idx, col_idx].set_title(f"{label}: Wordcloud")
                axes[row_idx, col_idx].axis("off")

        # Show plot
        plt.tight_layout()
        plt.show()

    def wordcount_heatmap_overlap(self):
        """Generate a heatmap showing the overlap in words between different texts."""
        texts = list(self.data['wordcount'].keys())  # texts
        num_texts = len(texts)  # how many texts we have, ex: 10 artists
        overlap_matrix = pd.DataFrame(0, index=texts, columns=texts)  # create empty matrix for plotting heatmap

        for i in range(num_texts):  # first artist
            for j in range(i + 1, num_texts):  # second artist
                if i == j:
                    continue  # skip this iteration of j loop if i = j (so when artist1 goes with artist1, the overlap is 0)
                # intersect lyrics btwn artist 1 and 2
                artist1 = set(self.data['wordcount'][texts[i]])  # get word count
                artist2 = set(self.data['wordcount'][texts[j]])  # get word count
                common_words = artist1.intersection(artist2)  # how many words in common

                # update matrix using .at function using the length of the common words
                overlap_matrix.at[texts[i], texts[j]] = len(common_words)
                overlap_matrix.at[texts[j], texts[i]] = len(common_words)

        # plot
        plt.figure(figsize=(18, 16))
        sns.heatmap(overlap_matrix, annot=True, cmap='viridis', fmt="d")
        plt.title("Lyric Overlap Heatmap")
        plt.show()