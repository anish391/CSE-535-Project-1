#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
#Necessary Tweepy Libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables required to access Twitter API

consumer_key='HBy7StkBrv0w67zlqRnnhvsPO'
consumer_secret='WFt5drHQMMfPFv09TgejJkKpciZwH5wMNNQptKvZY2FQsaSZ41'
access_token='105377073-QCwpfWm8L5NOBVq8XpWB6N1FvfeahQtGE37QHKjz'
access_token_secret='uMdsgCkAZyxgkySr8mXukeGpVT1e0aDXC4lg3Kdy9pbVp'

#Listen and print tweets	
class StdOutListener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        misc_list = []
        required_list = ["id", "text", "entities","retweeted"]
        print("{")
        if(data["retweeted"] == True):
            return True
        for key,value in data.items():
            if(key in required_list):
                if("extended_tweet" in data and key=="text"):
                    value = data["extended_tweet"]   
                value = str(value).encode("utf-8",errors='ignore')
                print('"'+key+'"' +": "+'"'+str(value).strip(" 'b\" ")+'" ,')
        print("}\n,")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    twitter_authentication = OAuthHandler(consumer_key, consumer_secret)
    twitter_authentication.set_access_token(access_token, access_token_secret)
    stream = Stream(twitter_authentication, l)
    
    #This line filter Twitter Streams to capture data by the keywords 'python', 'javascript', 'ruby'
    stream.filter(track=['global warming','pollution','climate change','sustainable','gas','environment'], languages=['en','es','ja'])
    
