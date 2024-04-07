"""
File: lyric_scraper.py
Description: Uses the lyricsgenius library to scrape for the lyrics of artists
             Files will get downloaded as .json in same directory as lyric_scraper.py
"""

from lyricsgenius import Genius

GENIUS_API_TOKEN='bcn9THJtfKp4ciCitw_-s7eq8pXq3aSwxsbX10NgiYMP3PnqXhOGqKGe5gC0UAm8'

ARTISTS = ['Kendrick Lamar', # names of artists to scrape for
            'Childish Gambino', 
            'Frank Ocean', 
            'Olivia Rodrigo', 
            'Radiohead',
            'Sabrina Carpenter', 
            'Beabadoobee', 
            'Clairo', 
            'Laufey', 
            'Lana Del Rey']

MAX_SONGS=50 # number of songs to scrape lyrics for from each artist
SORT='popularity' # how to sort songs to grab from artist (popularity or title)

def main():
    # list of artists to scrape for
    artist_names = ARTISTS

    # intialize Genius object
    genius = Genius(
        access_token=GENIUS_API_TOKEN, # API token
        remove_section_headers=True, # remove [Chorus], [Verse], etc... from lyrics
        skip_non_songs=True, # skip non-songs
        timeout=60 # seconds to wait for a response before erroring
    )

    # iterate over artists, grab the lyrics from the 50 most popular songs for each
    for artist_name in artist_names:
        artist = genius.search_artist(artist_name, max_songs=MAX_SONGS, sort=SORT)
        artist.save_lyrics(f'{artist_name.replace(" ", "").lower()}_lyrics',
                            extension='json',
                            overwrite=True)

if __name__ == '__main__':
    main()


