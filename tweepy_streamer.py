from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from matplotlib import pyplot as plt

import twitter_credentials
import analyze_data


class TwitterClient:

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = [tweet for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets)]
    # tweets = [tweet for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets)]
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = [friend for friend in Cursor(self.twitter_client.friends).items(num_friends)]
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = [tweet for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets)]
        return home_timeline_tweets


class TwitterAuthenticator():

    def __init__(self):
        pass

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def __init__(self):
        self.twitter_auth = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tags_list):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_auth.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords
        stream.filter(track=hash_tags_list)


class TwitterListener(StreamListener):
    """
    Basic listener class that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        super().__init__()
        self.filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print('Data: ' + data)  # JSON format
            with open(self.filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on_data: ' + str(e))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False on_data method in case rate limit occurs
            return False
        print('Error: ' + status_code)


if __name__ == '__main__':
    hash_tags = ['selectivitat', 'selectividad', 'universitat', 'universidad']
    filename = 'tweets.txt'

    # tweeter_streamer = TwitterStreamer()
    # tweeter_streamer.stream_tweets(filename, hash_tags)

    twitter_client = TwitterClient()
    tweet_analyzer = analyze_data.TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="introduce_user", count=20)
    print(tweets)
    # print(twitter_client.get_user_timeline_tweets(1))

    # print(dir(tweets[0]))  # All of the possible things we can ask for a tweet
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(10))

