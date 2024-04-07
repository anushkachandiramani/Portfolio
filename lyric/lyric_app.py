"""
File: lyric_app.py
Description: mainfile for running Lyric 
"""

from lyric import Lyric
import lyric_parsers as lp

def main():
    # intialize Lyric object
    lyric = Lyric()

    # load in stopwords
    lyric.load_stop_words('data/stopwords.txt')

    # load in song lyrics
    lyric.load_text('data/clairo_lyrics.json', 'Clairo', parser=lp.json_parser)
    lyric.load_text('data/lanadelrey_lyrics.json', 'Lana Del Rey', parser=lp.json_parser)
    lyric.load_text('data/beabadoobee_lyrics.json', 'Beabadoobee', parser=lp.json_parser)
    lyric.load_text('data/frankocean_lyrics.json', 'Frank Ocean', parser=lp.json_parser)
    lyric.load_text('data/laufey_lyrics.json', 'Laufey', parser=lp.json_parser)
    lyric.load_text('data/oliviarodrigo_lyrics.json', 'Olivia Rodrigo', parser=lp.json_parser)
    lyric.load_text('data/radiohead_lyrics.json', 'Radiohead', parser=lp.json_parser)
    lyric.load_text('data/sabrinacarpenter_lyrics.json', 'Sabrina Carpenter', parser=lp.json_parser)
    lyric.load_text('data/childishgambino_lyrics.json', 'Childish Gambino', parser=lp.json_parser)
    lyric.load_text('data/kendricklamar_lyrics.json', 'Kendrick Lamar', parser=lp.json_parser)

    # run visualizations
    lyric.wordcount_sankey()
    lyric.wordcount_wordcloud()
    lyric.wordcount_heatmap_overlap()

if __name__ == '__main__':
    main()