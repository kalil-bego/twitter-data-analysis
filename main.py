import tweepy
import os
import csv
from dotenv import load_dotenv
from datetime import datetime
from content import content

load_dotenv()
twitter_bearer_token = os.getenv(content['bearer_token_string'])

client = tweepy.Client(twitter_bearer_token)

date_in_datetime_format = datetime.today()
datareal= datetime.isoformat(date_in_datetime_format)

print(content['alert_message_string'])
query = input(content['input_string'])
tweets = tweepy.Paginator(
  client.search_recent_tweets,
  query=query,
  tweet_fields=['context_annotations', 'created_at'],
  end_time=(datareal+"Z"),
  max_results=100
).flatten(limit=1000)

with open(content['archive_name_string'], 'w', encoding='utf8') as csvfile:
  delimiter = ';'
  fieldnames = content['fieldnames_string']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
  writer.writeheader()
  for tweet in tweets:
    writer.writerow({
      content['fieldnames_string'][0]: tweet.text,
      content['fieldnames_string'][1]: tweet.created_at
    })