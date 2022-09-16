# DROP TABLES

games_table_drop = 'DROP TABLE IF EXISTS games;'
reviews_table_drop = 'DROP TABLE IF EXISTS reviews;'
review_authors_table_drop = 'DROP TABLE IF EXISTS review_authors;'

# CREATE TABLES

games_table_create = ("""
CREATE TABLE IF NOT EXISTS games (
appid bigint PRIMARY KEY,
name text NOT NULL,
developer text,
publisher text,
positive_review_count int,
negative_review_count int,
owners_range text,
average_forever_playtime int,
average_2weeks_playtime int,
median_forever_playtime int,
median_2weeks_playtime int,
languages text
);
""")

reviews_table_create = ("""
CREATE TABLE IF NOT EXISTS reviews (
recommendationid text PRIMARY KEY,
appid bigint NOT NULL,
author_steamid text NOT NULL,
language text,
review text,
timestamp_created timestamp,
timestamp_updated timestamp,
voted_up boolean,
votes_up bigint,
votes_funny bigint,
weighted_vote_score text,
comment_count bigint,
steam_purchase boolean,
received_for_free boolean,
written_during_early_access boolean
);
""")

review_authors_table_create = ("""
CREATE TABLE IF NOT EXISTS review_authors (
steamid text,
recommendationid text,
num_games_owned int NOT NULL,
num_reviews int NOT NULL,
playtime_forever text,
playtime_last_two_weeks text,
playtime_at_review text,
last_played_at timestamp,
PRIMARY KEY (steamid, recommendationid)
);
""")

# INSERT RECORDS

games_table_insert = ("""
INSERT INTO games (appid, name, developer, publisher, positive_review_count, negative_review_count, owners_range,
                    average_forever_playtime, average_2weeks_playtime, median_forever_playtime, median_2weeks_playtime, languages)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (appid) DO NOTHING;
""")

reviews_table_insert = ("""
INSERT INTO reviews (recommendationid, appid, author_steamid, language, review, timestamp_created, timestamp_updated, voted_up,
                    votes_up, votes_funny, weighted_vote_score, comment_count, steam_purchase, received_for_free, written_during_early_access)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (recommendationid) DO NOTHING;
""")

review_authors_table_insert = ("""
INSERT INTO review_authors (steamid, recommendationid, num_games_owned, num_reviews, playtime_forever,
                            playtime_last_two_weeks, playtime_at_review, last_played_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (steamid, recommendationid) DO NOTHING;
""")

# QUERY LISTS

create_table_queries = [games_table_create, reviews_table_create, review_authors_table_create]
drop_table_queries = [games_table_drop, reviews_table_drop, review_authors_table_drop]