from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
from textblob import TextBlob
import nltk
import string
from nltk.corpus import stopwords
from datetime import datetime
now = datetime.now()
import requests
filenames=now.strftime('%Y_%m_%d_%H_%M')
CONSUMER_KEY = "LJpGAdgt9QURuUl3KiR0DNP9d"
CONSUMER_SECRET = "azsenE7EcfOXodDkE64WuTuDZKZoV5cYzPhnAAr44Pb6rCHgJS"
ACCESS_TOKEN = "779531845256044545-WLJ1BGlMxeVolPnSKbiTfS2GrXe0ZyC"
ACCESS_TOKEN_SECRET = "Yxc76sIfx1UPPaUtQV1xPzW2o10ymY6g1BxuMuenKIkPr"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


# # # # TWITTER CLIENT # # # #
class TwitterExtract():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def searcht(self, api, query, max_tweets):
        searched_tweets = []
        last_id = -1
        geocode = '5,-74,500km'
        while len(searched_tweets) < max_tweets:
            count = max_tweets - len(searched_tweets)
            try:
                new_tweets = api.search(q=query, geocode=geocode, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break
                searched_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # depending on TweepError.code, one may want to retry or wait
                # to keep things simple, we will give up on an error
                break
        return searched_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def wordCounter(self,tweet):
        return len(nltk.word_tokenize(str(tweet), language='spanish'))


    def trastalteToEng(self,tweet):
        # url = 'http://translate.google.com/translate_a/t'
        # params = {
        #     "text":tweet,
        #     "sl": "es",
        #     "tl": "en",
        #     "client": "p"
        # }
        # engjo=requests.get(url, params=params).content
        totraslate=TextBlob(self.clean_tweet(tweet))
        eng = totraslate.translate(to='en')
        engjo = ''.join(eng)
        return engjo

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df




    def cleanTweetF(self,df):
        union = ' '.join(df.tweets)
        tokens = nltk.word_tokenize(union, language='spanish')
        punctuations = list(string.punctuation)
        clean_tokens = tokens[:]
        sr = stopwords.words('spanish')
        for token in tokens:
            if token in sr:
                clean_tokens.remove(token)
            if token in punctuations:
                clean_tokens.remove(token)
            if token == 'https':
                clean_tokens.remove(token)
            if token.startswith('//t'):
                clean_tokens.remove(token)
            if token == 'RT':
                clean_tokens.remove(token)
        cleaned = " ".join(clean_tokens)
        all = nltk.word_tokenize(cleaned, language='spanish')
        return all


def runall(query, maxt):

    twitter_extract = TwitterExtract()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_extract.get_twitter_client_api()

    tweets = twitter_extract.searcht(api, query, maxt)

    df = tweet_analyzer.tweets_to_data_frame(tweets)

    df['Words'] = df['tweets'].apply(tweet_analyzer.wordCounter)
    df['English'] = np.array([tweet_analyzer.trastalteToEng(tweet) for tweet in df['tweets']])
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['English']])
    # freq
    freq = nltk.FreqDist(tweet_analyzer.cleanTweetF(df))
    plot = freq.plot(20, cumulative=False)
    fig = plot.get_figure()
    # fig.close()
    fig.figsize=[6.4, 4.8]
    fig.savefig("static/graphics/freq.png")
    # pie matplot
    # labels = list(df['source'].unique())
    # cant = list(df['source'].value_counts())
    # fig1, ax1 = plt.subplots()
    # ax1.pie(cant, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #
    # plt.savefig('static/images/foo.png')
    return df
