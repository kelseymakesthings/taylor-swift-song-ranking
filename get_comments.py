import argparse
import json
import os
import re

from collections import Counter
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import urlopen

YT_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'

# These are YouTube urls of folklore lyric videos.
# Change to whatever album/videos you want to.
NAMES_TO_URL = {
    'the 1': 'https://www.youtube.com/watch?v=KsZ6tROaVOQ',
    'cardigan': 'https://www.youtube.com/watch?v=zLSUp53y-HQ', # Note: this is the lyric video, not music video
    'the last great american dynasty': 'https://www.youtube.com/watch?v=2s5xdY6MCeI',
    'exile': 'https://www.youtube.com/watch?v=osdoLjUNFnA',
    'my tears ricochet': 'https://www.youtube.com/watch?v=OWbDJFtHl3w',
    'mirrorball': 'https://www.youtube.com/watch?v=KaM1bCuG4xo',
    'seven': 'https://www.youtube.com/watch?v=pEY-GPsru_E',
    'august': 'https://www.youtube.com/watch?v=nn_0zPAfyo8',
    'this is me trying': 'https://www.youtube.com/watch?v=9bdLTPNrlEg',
    'illicit affairs': 'https://www.youtube.com/watch?v=MLV2SJKWk4M',
    'invisible string': 'https://www.youtube.com/watch?v=OuFnpmGwg5k',
    'mad woman': 'https://www.youtube.com/watch?v=6DP4q_1EgQQ',
    'epiphany': 'https://www.youtube.com/watch?v=DUnDkI7l9LQ',
    'betty': 'https://www.youtube.com/watch?v=6TAPqXkZW_I',
    'peace': 'https://www.youtube.com/watch?v=HpxX4ZE4KWE',
    'hoax': 'https://www.youtube.com/watch?v=ryLGxpjwAhM',
}


def get_comments(yt_url):
    # Referencing https://github.com/srcecde/python-youtube-api
    def load_comments():
        comments_arr = []
        for item in mat['items']:
            comment = item['snippet']['topLevelComment']
            text = comment['snippet']['textDisplay']
            comments_arr.append(text)
        return comments_arr

    def open_url(url, params):
        f = urlopen(url + '?' + urlencode(params))
        data = f.read()
        f.close()
        matches = data.decode('utf-8')
        return matches

    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Required API key')
    args = parser.parse_args()
    if not args.key:
        exit('Please specify API key using the --key=parameter.')

    video_id = urlparse(str(yt_url))
    q = parse_qs(video_id.query)
    vid = q['v'][0]

    params = {
        'part': 'snippet,replies',
        'videoId': vid,
        'key': args.key
    }
    all_comments = []
    matches = open_url(YT_COMMENT_URL, params)
    mat = json.loads(matches)
    next_pg_token = mat.get('nextPageToken')
    this_pg_comments = load_comments()
    all_comments.extend(this_pg_comments)
    pg_count = 1
    comment_count = len(this_pg_comments)
    while next_pg_token:
        if pg_count % 10 == 0:
            print(f'Loaded {pg_count} pages of comments, {comment_count} total comments')
        params.update({'pageToken': next_pg_token})
        matches = open_url(YT_COMMENT_URL, params)
        mat = json.loads(matches)
        next_pg_token = mat.get('nextPageToken')
        this_pg_comments = load_comments()
        all_comments.extend(this_pg_comments)
        pg_count += 1
        comment_count += len(this_pg_comments)
    return all_comments

def write_comments(all_comments, file_name):
    # Takes list of all comments and outputs to
    # specified filename
    with open(file_name, 'w+') as f:
        for comment in all_comments:
            f.write(comment + '\n')

def get_most_common_words(comment_file):
    # Generate a dict of words to counts from file of raw comments
    with open(comment_file) as f:
        all_comments = f.read()
        words = re.findall(r'\w+', all_comments)
        # You can find most common sequences of 2 words with:
        # re.findall(r'\w+ \w+', all_comments)
        # and so on
        words_upper = [word.upper() for word in words] # Disregard case of words
        word_counts = Counter(words_upper)
        return word_counts

def write_most_common_words(word_counts, file_name):
    # Takes dict of words to counts and outputs to 
    # specified filename in descending order
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    with open(file_name, 'w+') as f:        
        for word, count in sorted_words:
            f.write(f'{word}, {count}\n')    

if __name__ == '__main__':
    if not os.path.exists('comments'):
        # Create comments directory
        os.makedirs('comments')

    for name, song_url in NAMES_TO_URL.items():
        print('Getting comments for song:', name)
        comment_file = 'comments/' + name.replace(' ', '_') + '_comments.txt'
        write_comments(get_comments(song_url), comment_file)
        print('Comments saved to', comment_file)

        print('Getting most common words')
        words_file = 'comments/' + name.replace(' ', '_') + '_words.txt'
        write_most_common_words(get_most_common_words(comment_file), words_file)
        print('Common words saved to', words_file)
