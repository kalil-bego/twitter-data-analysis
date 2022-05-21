import tweepy
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from os import path
from dotenv import load_dotenv
from datetime import datetime
from wordcloud import WordCloud, STOPWORDS
from resources.content import stop_words

class DataTwitter:

  def __init__(self, query, limit):
    load_dotenv()
    twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    self.query = query
    self.limit = limit
    self.client = tweepy.Client(twitter_bearer_token)
    self.stopwords = set(STOPWORDS)
    self.stopwords.update(stop_words)
    self.directory = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

  def find_recent_tweets(self):
    date_in_datetime_format = datetime.today()
    datareal = datetime.isoformat(date_in_datetime_format)

    return tweepy.Paginator(
      self.client.search_recent_tweets,
      query=self.query,
      tweet_fields=['context_annotations', 'created_at', 'source'],
      end_time=(datareal+"Z"),
      max_results=100
    ).flatten(self.limit)

  def save_csv_archive(self, tweets, filename, fieldnames, delimiter=';'):
    with open(filename, 'w', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
      writer.writeheader()
      for tweet in tweets:
        writer.writerow({
          fieldnames[0]: tweet.text,
          fieldnames[1]: tweet.created_at,
          fieldnames[2]: tweet.source
        })

  def show_word_cloud(self, filename, delimiter=';', maskpath='resources/images/twitter_logo.png'):
    comment_words = ''
    mask = np.array(Image.open(path.join(self.directory, maskpath)))

    with open(filename, 'r', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile, delimiter=delimiter)
      for row in reader:
        tokens = row[0].split()
          
        for i in range(len(tokens)):
          tokens[i] = tokens[i].lower()
          
      comment_words += " ".join(tokens)+" "
      self.__plot_graphic(
        WordCloud(
          background_color="white",
          max_font_size=60,
          mask = mask,
          margin = 10,
          stopwords = self.stopwords,
        ).generate(comment_words)
      )

  def __plot_graphic(self, content):
    plt.figure()
    plt.title(self.query)
    plt.imshow(content, interpolation='bilinear')
    plt.axis("off")
    plt.show()