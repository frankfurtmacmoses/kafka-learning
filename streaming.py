from __future__ import absolute_import
#import tweepy #.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream,API
from kafka import KafkaProducer
import json
import yaml
from datetime import datetime, timedelta
import time
#import pickle   

def do_login():
    with open('config.yaml') as file:
        authentication = yaml.full_load(file)
        print(" ")
        print("---------------------------------")
        print(" ")
        print("Successfully loaded configuration")
        access_token = authentication[0].get('access_token')
        access_token_secret = authentication[1].get('access_token_secret')
        api_key = authentication[2].get('api_key')
        api_key_secret = authentication[3].get('api_key_secret')
        auth = OAuthHandler(api_key,api_key_secret)
        auth.set_access_token(access_token,access_token_secret)
        api = API(auth)
        print(api.verify_credentials().screen_name)
        print(" ")
        print("---------------------------------")
        print(" ")
        print("Successfully logon to twitter")
        return api
## Helper method for time 

def normalize_timestamp(time):
    mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    mytime += timedelta(hours=1)   # the tweets are timestamped in GMT timezone, while I am in +1 timezone
    return (mytime.strftime("%Y-%m-%d %H:%M:%S")) 

def get_twitter_data():
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic_name = 'appletopics'
    api = do_login()
    print(" ")
    print("Now collecting tweets ............ ")
    res = api.search_tweets("Apple OR iphone OR iPhone")
    for i in res:
        
        user_id =  str(i.user.id_str)
        user_name = str(i.user.name)
        number_of_follower = str(i.user.followers_count)
        location = str(i.user.location)
        nubmer_of_time_retweeted = str(i.retweet_count)
        created_at = str(i.user.created_at)

        # Create a dictionary record
        record = {'user':user_id,'user_name':user_name, 'number_of_follower':number_of_follower,'location': location, 'nubmer_of_time_retweeted':nubmer_of_time_retweeted,'created_at':created_at}
        # send record to kakfka
        producer.send(topic_name, record)
             
def periodic_work(interval):
    while True:
        get_twitter_data()
        #interval should be an integer, the number of seconds to wait
        time.sleep(interval)


if __name__ == "__main__":
    do_login()
    periodic_work(60 * 0.1)
  