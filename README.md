# taylor-swift-song-ranking

Rank songs using YouTube metrics and scrape comments (used on Taylor Swift's albums evermore, folklore, and Lover).

## How to start:

1.  Clone this project with `git clone https://github.com/kelseymakesthings/taylor-swift-song-ranking.git`
2.  `cd taylor-swift-song-ranking`
3.  Install dependencies: `pip install -r requirements.txt`
4.  Make a new project on Google develeper console, allow YouTube Data API access, create credentials. More info [here](https://developers.google.com/youtube/v3/getting-started) and [here](https://developers.google.com/youtube/v3/quickstart/python)

## To get current ranking of songs:

Run `python get_ranking.py`.
This will print out the ranking of all songs' YouTube lyric videos, with associated scores.

## To scrape comments and find most common words/sequences of words:

Run `python get_comments.py`.
This will save all comments and common words into files in the `comments/` directory.
