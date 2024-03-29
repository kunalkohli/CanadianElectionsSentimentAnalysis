import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, queries, count = 20): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 

        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = []
            for query in queries:
              fetched_tweets.append(self.api.search(q = query, count = count))
            print(len(fetched_tweets))
            # parsing tweets one by one 
            for index in range(len(fetched_tweets)):
              for tweet in fetched_tweets[index]: 
                  # empty dictionary to store required params of a tweet 
                  parsed_tweet = {} 
                  #print(tweet)
                  # saving text of tweet 
                  parsed_tweet['text'] = tweet.text 
                  # saving sentiment of tweet 
                  parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

                  # appending parsed tweet to tweets list 
                  if tweet.retweet_count > 0: 
                      # if tweet has retweets, ensure that it is appended only once 
                      if parsed_tweet not in tweets: 
                          tweets.append(parsed_tweet) 
                  else: 
                      tweets.append(parsed_tweet) 

            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 


def main(queries,num_tweets): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 

    tweets = api.get_tweets(queries = queries, count = num_tweets)
    #print(tweets)

    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    positive_tweets_per = (100*len(ptweets)/len(tweets))
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    megative_tweets_per = (100*len(ntweets)/len(tweets))
    #print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    neutral_tweets_per = (100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))
    #print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
  
    # print("\n\nPositive tweets:") 
    # for tweet in ptweets[:10]: 
    #     print(tweet['text']) 
  
    # # printing first 5 negative tweets 
    # print("\n\nNegative tweets:") 
    # for tweet in ntweets[:10]: 
    #     print(tweet['text']) 

    tweet_return_dict = {}
    tweet_return_dict['Positive_perc'] = positive_tweets_per
    tweet_return_dict['Negative_perc'] = megative_tweets_per
    tweet_return_dict['Neutral_perc'] = neutral_tweets_per

    return (tweet_return_dict)


if __name__ == "__main__": 
  # calling main function 


  Scheer_sentiment = main(queries = ['#AndrewScheer'], num_tweets = 1000) #change number of tweets here
  print('Scheer Sentiment Score ' , Scheer_sentiment)

  Trudeau_Black_Face_sentiment = main(queries = ['#BlackfaceTrudeau','#Trudeaublackface','#JustinTrudeau'], num_tweets = 1000) #change number of tweets here
  print('Trudeau_Black_Face_sentiment Sentiment Score ' , Trudeau_Black_Face_sentiment)


