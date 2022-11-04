from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream,API
from kafka import KafkaProducer
import json
import yaml
from datetime import datetime, timedelta
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'apple-tweets'

with open('config.yaml') as file:
    try:
        authentication = yaml.safe_load()
        print("successfully loaded configuration")
    except yaml.error as exception:
        print(exception)

access_token = authentication.access_token
access_token_secret = authentication.access_token_secret
api_key =  authentication.api_key
api_secret =  authentication.api_secret
auth = OAuthHandler(api_key,api_secret)
auth.set_access_token(access_token,access_token_secret)
api = API(auth)

## Helper method for time 
def normalize_timestamp(time):
    mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    mytime += timedelta(hours=1)   # the tweets are timestamped in GMT timezone, while I am in +1 timezone
    return (mytime.strftime("%Y-%m-%d %H:%M:%S")) 

def get_twitter_data():
    rec = {}
    res = api.search("Apple OR iphone OR iPhone")
    for i in res:
        record = ''
        record += str('user:' + i.user.id_str)
        record += ' '
        record += str('time:' + normalize_timestamp(str(i.created_at)))
        record += ' '
        record += str('number_of_follower:'+ i.user.followers_count)
        record += ' '
        record += str('location:'+ i.user.location)
        record += ' '
        record += str('nubmer_of_time_retweeterd:'+ i.retweet_count)
        record += ' '
        rec.add(record)
        producer.send(topic_name, str.encode(rec))
        rec = {}
             
def periodic_work(interval):
    while True:
        get_twitter_data()
        #interval should be an integer, the number of seconds to wait
        time.sleep(interval)


if __name__ == "__main__":
   periodic_work(60 * 0.1)