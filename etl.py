# repurposed from 'Data Modelling with Postgres' activity

import os
import glob
import psycopg2
import pandas as pd
import json
from pandas.io.json import json_normalize
from sql_queries import *


def process_games_file(cur, filepath):
    """
    This function processes the 'steam_spy_detailed.csv' file whose filepath has been provided as an arugment.
    It extracts the game information in order to store it into the games table.
    Then it extracts the game tag information in order to store it into the game_tags table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # open games file
    df = pd.read_csv(filepath)

    # insert games record
    game_data = df[ ['appid', 'name', 'developer', 'publisher', 'positive', 'negative', 'owners',
                     'average_forever', 'average_2weeks', 'median_forever', 'median_2weeks', 'languages'] ]
    game_data.dropna(subset=['name', 'developer', 'languages'], inplace=True)

    for i, row in game_data.iterrows():
        cur.execute(games_table_insert, row)

def process_reviews_file(cur, filepath):
    """
    This function processes a reviews file whose filepath has been provided as an argument.
    It converts epoch timestamps to datetime and then prepares to insert records into the reviews and review_authors tables.
    """
    # open reviews file
    f = open(filepath)
    js = json.load(f)
    df = json_normalize(js['reviews'])
    df['timestamp_created'] = pd.to_datetime(df[ 'timestamp_created' ], unit = 's').apply(str)
    df['timestamp_updated'] = pd.to_datetime(df[ 'timestamp_updated' ], unit = 's').apply(str)
    df['author.last_played'] = pd.to_datetime(df[ 'author.last_played' ], unit = 's').apply(str)
    df['appid'] = os.path.basename(os.path.dirname(filepath))

    # insert reviews record
    reviews_data = df[ ['recommendationid', 'appid', 'author.steamid', 'language', 'review', 'timestamp_created',
                        'timestamp_updated', 'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score',
                        'comment_count', 'steam_purchase', 'received_for_free', 'written_during_early_access'] ]

    for i, row in reviews_data.iterrows():
        cur.execute(reviews_table_insert, row)

    # insert review_authors record
    review_authors_data = df[ ['author.steamid', 'recommendationid', 'author.num_games_owned',
                               'author.num_reviews', 'author.playtime_forever', 'author.playtime_last_two_weeks',
                               'author.playtime_at_review', 'author.last_played'] ]

    for i, row in review_authors_data.iterrows():
        cur.execute(review_authors_table_insert, row)

def process_data(cur, conn, filepath, filetype, func):
    """
    This procedure iterates through all the files that need to be processed,
    and prints out a status/progress message.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, filetype))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    """
    This procedure connects to the steam_reviews database and executes the functions defined above.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=steam_reviews user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/games', filetype='*.csv', func=process_games_file)
    process_data(cur, conn, filepath='data/reviews', filetype='*.json', func=process_reviews_file)

    conn.close()


if __name__ == "__main__":
    main()