import tweepy
import os
import csv
from dotenv import load_dotenv
from datetime import datetime

class DataTwitter:

  def __init__(self, query):
    load_dotenv()
    twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    self.query = query
    self.client = tweepy.Client(twitter_bearer_token)
    self.auth = tweepy.OAuth2BearerHandler(twitter_bearer_token)

  def find_recent_tweets(self):
    date_in_datetime_format = datetime.today()
    datareal = datetime.isoformat(date_in_datetime_format)

    return tweepy.Paginator(
      self.client.search_recent_tweets,
      query=self.query,
      tweet_fields=['context_annotations', 'created_at', 'source'],
      end_time=(datareal+"Z"),
      max_results=100
    ).flatten(limit=1000)

  def save_csv_archive(self, tweets, name, fieldnames, delimiter=';'):
    with open(name, 'w', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
      writer.writeheader()
      for tweet in tweets:
        writer.writerow({
          fieldnames[0]: tweet.text,
          fieldnames[1]: tweet.created_at,
          fieldnames[2]: tweet.source
        })